/**
 * API 호출을 담당하는 모듈입니다.
 * 각 함수는 백엔드 API 명세의 요구사항 ID를 주석으로 포함합니다.
 */

const API_BASE = '';

const apis = {
    isRefreshing: false,
    refreshSubscribers: [],

    subscribeTokenRefresh(cb) {
        this.refreshSubscribers.push(cb);
    },

    onTokenRefreshed(token) {
        this.refreshSubscribers.map(cb => cb(token));
        this.refreshSubscribers = [];
    },

    async request(url, options = {}, skipAlert = false) {
        const headers = { ...options.headers };
        if (state.token) {
            headers['Authorization'] = `Bearer ${state.token}`;
        }

        try {
            const response = await fetch(`${API_BASE}${url}`, { ...options, headers });
            
            // 401 Unauthorized 처리 (토큰 만료 시 리프레시 시도)
            if (response.status === 401) {
                // 로그인 요청에서 401은 리프레시 대상이 아님
                if (url === '/auth/login') {
                    return { status: 401 };
                }
                
                // 토큰이 없는 경우 리프레시 시도 없이 로그아웃
                if (!state.token) {
                    await logout();
                    return null;
                }

                // 이미 리프레시 중이면 대기열에 추가
                if (this.isRefreshing) {
                    return new Promise((resolve) => {
                        this.subscribeTokenRefresh(token => {
                            headers['Authorization'] = `Bearer ${token}`;
                            resolve(this.request(url, options, skipAlert));
                        });
                    });
                }

                this.isRefreshing = true;
                try {
                    const refreshResponse = await fetch(`${API_BASE}/users/refresh`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' }
                    });

                    if (refreshResponse.ok) {
                        const data = await refreshResponse.json();
                        state.token = data.access_token;
                        localStorage.setItem('token', state.token);
                        
                        this.isRefreshing = false;
                        this.onTokenRefreshed(state.token);
                        
                        // 원래 요청 재시도
                        headers['Authorization'] = `Bearer ${state.token}`;
                        return await this.request(url, options, skipAlert);
                    } else {
                        // 리프레시 실패 시 로그아웃
                        this.isRefreshing = false;
                        await logout();
                        return null;
                    }
                } catch (refreshErr) {
                    this.isRefreshing = false;
                    await logout();
                    return null;
                }
            }
            
            if (!response.ok) {
                let error;
                try {
                    error = await response.json();
                } catch (e) {
                    error = { detail: '서버 응답 처리 중 오류가 발생했습니다.' };
                }
                
                let msg = error.detail || '요청 중 오류가 발생했습니다.';
                if (Array.isArray(msg)) {
                    msg = msg.map(e => {
                        let text = e.msg;
                        text = text.replace(/^Value error, /, '');
                        text = text.replace(/^Field required, /, '');
                        if (text === 'Field required') text = '필수 입력 항목입니다.';
                        return text;
                    }).join(', ');
                }

                // 특정 메시지 처리
                const passwordErrorMessage = "비밀번호는 대소문자, 특수문자, 숫자를 각 1개씩 포함한 8자리 이상이어야 합니다.";
                if (msg.includes(passwordErrorMessage)) {
                    msg = passwordErrorMessage;
                } else if (response.status >= 500) {
                    msg = "잠시후 다시 시도해주세요.";
                }

                const errObj = new Error(msg);
                errObj.status = response.status;
                throw errObj;
            }
            if (response.status === 204) return null;
            return await response.json();
        } catch (err) {
            if (url !== '/auth/login' && !skipAlert) {
                utils.showAlert(err.message, 'error', '오류');
            }
            throw err;
        }
    },

    // --- Auth & Users ---
    /**
     * 회원가입
     * [REQ-USER-001] 사내 구성원은 이메일, 비밀번호, 이름, 소속 부서, 성별, 전화번호를 입력하여 회원가입을 할 수 있다.
     */
    async signup(userData) {
        return await this.request('/users/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        }, true);
    },

    /**
     * 로그인
     * [REQ-USER-002] 가입된 이메일과 비밀번호로 로그인을 할 수 있다.
     */
    async login(email, password) {
        return await this.request('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }, true);
    },


    /**
     * 토큰 갱신
     * [NFR-USER-001] 로그인 성공 시 Access Token(JSON Body)과 Refresh Token(HTTP-only Cookie)이 발급된다.
     */
    async refresh() {
        return await fetch(`${API_BASE}/users/refresh`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
    },

    /**
     * 로그아웃
     * [REQ-USER-003] 로그인된 사용자는 로그아웃을 할 수 있다.
     */
    async logout() {
        return await this.request('/users/logout', { method: 'POST' });
    },

    /**
     * 내 정보 조회
     * [REQ-USER-006] 로그인된 사용자는 본인의 정보를 조회할 수 있다.
     */
    async getMe() {
        return await this.request('/users/me');
    },

    /**
     * 내 정보 수정
     * [REQ-USER-007] 로그인된 사용자는 본인의 정보(부서, 전화번호)를 수정할 수 있다.
     */
    async updateMe(userData) {
        return await this.request('/users/me', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        }, true);
    },

    /**
     * 비밀번호 변경
     * [REQ-USER-008] 로그인된 사용자는 본인의 비밀번호를 변경할 수 있다.
     */
    async updatePassword(passwordData) {
        return await this.request('/users/me/password', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(passwordData)
        }, true);
    },

    /**
     * 회원 탈퇴
     * [REQ-USER-009] 로그인된 사용자는 회원 탈퇴를 할 수 있다.
     */
    async deleteMe() {
        return await this.request('/users/me', { method: 'DELETE' });
    },

    // --- Patients ---

    /**
     * 환자 등록
     * [REQ-PTNT-001] 사내 의료인 역할을 가진 유저만 환자를 신규 등록할 수 있다.
     */
    async createPatient(patientData) {
        return await this.request('/patients', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(patientData)
        });
    },

    /**
     * 환자 목록 조회
     * [REQ-PTNT-002] 로그인된 사내 개발진, 의료 실무진, 연구진은 환자 목록을 조회할 수 있다.
     */
    async getPatients(params = {}) {
        const query = new URLSearchParams(params).toString();
        return await this.request(`/patients${query ? `?${query}` : ''}`);
    },

    /**
     * 환자 상세 조회
     * [REQ-PTNT-003] 특정 환자의 상세 정보를 조회할 수 있다.
     */
    async getPatient(patientId) {
        return await this.request(`/patients/${patientId}`);
    },

    /**
     * 환자 정보 수정
     * [REQ-PTNT-004] 특정 환자의 정보를 수정할 수 있다.
     */
    async updatePatient(patientId, patientData) {
        return await this.request(`/patients/${patientId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(patientData)
        });
    },

    /**
     * 환자 삭제
     * [REQ-PTNT-005] 특정 환자 정보를 삭제할 수 있다.
     */
    async deletePatient(patientId) {
        return await this.request(`/patients/${patientId}`, { method: 'DELETE' });
    },

    // --- Medical Records ---

    /**
     * 진료 기록 등록
     * [REQ-MDR-001] 사내 의료인 역할을 가진 유저만 환자의 진료 기록을 등록할 수 있다.
     */
    async createMedicalRecord(formData) {
        return await this.request('/medical-records', {
            method: 'POST',
            body: formData
        });
    },

    /**
     * 환자별 진료 기록 목록 조회
     * [REQ-MDR-002] 특정 환자의 진료 기록 목록을 조회할 수 있다.
     */
    async getPatientMedicalRecords(patientId) {
        return await this.request(`/patients/${patientId}/medical-records`);
    },

    /**
     * 진료 기록 상세 조회
     * [REQ-MDR-003] 특정 진료 기록의 상세 내용을 조회할 수 있다.
     */
    async getMedicalRecord(patientId, recordId) {
        return await this.request(`/patients/${patientId}/medical-records/${recordId}`);
    },

    // --- AI Prediction ---

    /**
     * AI 폐렴 예측 수행
     * [REQ-PRED-001] 진료기록에 등록된 X-ray 이미지를 활용하여 폐렴 여부를 예측한다.
     */
    async predictPneumonia(patientId, recordId) {
        return await this.request(`/patients/${patientId}/medical-records/${recordId}/ai-predictions`,
            { method: 'POST' },
            true
        );
    },

    /**
     * AI 예측 결과 목록 조회
     * [REQ-PRED-002] 특정 진료기록에 대해 수행된 모든 AI 예측 결과 목록을 조회한다.
     */
    async getMedicalRecordAnalyses(patientId, recordId) {
        return await this.request(`/patients/${patientId}/medical-records/${recordId}/ai-predictions`);
    },

    // --- Admin ---

    /**
     * 전체 유저 목록 조회 (관리자 전용)
     * [REQ-USER-004] 관리자 권한을 가진 유저는 전체 유저 목록을 조회할 수 있다.
     */
    async adminGetUsers(params = {}) {
        const query = new URLSearchParams(params).toString();
        return await this.request(`/admin/users${query ? `?${query}` : ''}`);
    },

    /**
     * 유저 권한 수정 (관리자 전용)
     * [REQ-USER-005] 관리자 권한을 가진 유저는 다른 유저의 권한을 수정할 수 있다.
     */
    async adminUpdateUserRole(roleData) {
        return await this.request('/admin/users/role', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(roleData)
        });
    }
};
