/**
 * 페이지 렌더링 및 이벤트 핸들러 모음
 */

const pages = {
    async renderHome() {
        const html = await utils.loadTemplate('home');
        if (state.currentPage !== '/' && state.currentPage !== '/home') return;
        const app = document.getElementById('app');
        app.innerHTML = html;
        
        const actions = document.getElementById('home-actions');
        if (!state.user) {
            actions.innerHTML = '<button onclick="navigate(\'/login\')">로그인하여 시작하기</button>';
        } else if (state.user.role === 'pending') {
            actions.innerHTML = '<p>관리자의 승인을 기다리는 중입니다.</p>';
        } else {
            actions.innerHTML = '<button onclick="navigate(\'/patients\')">환자 목록 보기</button>';
        }
    },

    async renderLogin() {
        const html = await utils.loadTemplate('login');
        document.getElementById('app').innerHTML = html;
    },

    async renderSignup() {
        const html = await utils.loadTemplate('signup');
        document.getElementById('app').innerHTML = html;
        
        const phoneInput = document.getElementById('signup-phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', (e) => utils.handlePhoneInput(e));
        }
    },

    async renderPatients(params = {}) {
        const patients = await apis.getPatients(params);
        const html = await utils.loadTemplate('patients');
        if (state.currentPage !== '/patients') return;
        const app = document.getElementById('app');
        app.innerHTML = html;

        // 필드 값 복원
        const nameInput = document.getElementById('search-name');
        const genderSelect = document.getElementById('filter-gender');
        const minAgeInput = document.getElementById('filter-min-age');
        const maxAgeInput = document.getElementById('filter-max-age');

        if (nameInput && params.name) nameInput.value = params.name;
        if (genderSelect && params.gender) genderSelect.value = params.gender;
        if (minAgeInput && params.min_age) minAgeInput.value = params.min_age;
        if (maxAgeInput && params.max_age) maxAgeInput.value = params.max_age;
        
        const listBody = document.getElementById('patients-list');
        if (patients.length === 0) {
            listBody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem;">검색 결과가 없습니다.</td></tr>';
            return;
        }
        listBody.innerHTML = patients.map(p => `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.age}</td>
                <td>${p.gender === 'male' ? '남성' : '여성'}</td>
                <td>${utils.formatPhoneNumber(p.phone_number)}</td>
                <td><button onclick="navigate('/patients/${p.id}')">상세보기</button></td>
            </tr>
        `).join('');
    },

    async renderPatientCreate() {
        const html = await utils.loadTemplate('patient-create');
        document.getElementById('app').innerHTML = html;
        
        const phoneInput = document.getElementById('phone_number');
        if (phoneInput) {
            phoneInput.addEventListener('input', (e) => utils.handlePhoneInput(e));
        }
    },

    async renderPatientDetail(patientId) {
        const patient = await apis.getPatient(patientId);
        const records = await apis.getPatientMedicalRecords(patientId);
        const html = await utils.loadTemplate('patient-detail');
        if (!state.currentPage.startsWith('/patients/')) return;
        const app = document.getElementById('app');
        app.innerHTML = html;
        
        // 환자 정보 표시
        document.getElementById('patient-name').innerText = `${patient.name} (${patient.gender === 'male' ? '남성' : '여성'})`;
        document.getElementById('patient-info').innerText = `나이: ${patient.age}세 | 연락처: ${utils.formatPhoneNumber(patient.phone_number)}`;
        
        // 수정 폼 초기값 설정
        document.getElementById('update-name').value = patient.name;
        document.getElementById('update-phone').value = utils.formatPhoneNumber(patient.phone_number);
        
        const updatePhoneInput = document.getElementById('update-phone');
        if (updatePhoneInput) {
            updatePhoneInput.addEventListener('input', (e) => utils.handlePhoneInput(e));
        }
        
        // 버튼 이벤트 바인딩
        document.getElementById('add-record-btn').onclick = () => navigate(`/patients/${patientId}/medical-records/create`);
        
        // 상세 페이지 전용 상태 (ID 저장)
        state.currentPatientId = patientId;

        const listBody = document.getElementById('records-list');
        listBody.innerHTML = records.map(r => `
            <tr>
                <td>${r.id}</td>
                <td>${r.chart_number}</td>
                <td>${r.symptoms}</td>
                <td>${new Date(r.created_at).toLocaleString()}</td>
                <td><button onclick="navigate('/patients/${patientId}/medical-records/${r.id}')">상세보기</button></td>
            </tr>
        `).join('');
    },

    async renderRecordCreate(patientId) {
        const html = await utils.loadTemplate('record-create');
        const app = document.getElementById('app');
        app.innerHTML = html;
        
        const imageInput = document.getElementById('xray_image');
        const previewContainer = document.getElementById('image-preview-container');

        imageInput.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    previewContainer.innerHTML = `<img src="${event.target.result}" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">`;
                };
                reader.readAsDataURL(file);
            } else {
                previewContainer.innerHTML = '<p>이미지 미리보기가 여기에 표시됩니다.</p>';
            }
        };

        document.getElementById('record-create-form').onsubmit = (e) => this.handleRecordCreate(e, patientId);
        document.getElementById('cancel-btn').onclick = () => navigate(`/patients/${patientId}`);
    },

    async renderRecordDetail(patientId, recordId) {
        const record = await apis.getMedicalRecord(patientId, recordId);
        const analyses = await apis.getMedicalRecordAnalyses(patientId, recordId);
        const html = await utils.loadTemplate('record-detail');
        const app = document.getElementById('app');
        app.innerHTML = html;
        
        document.getElementById('record-id').innerText = record.id;
        document.getElementById('chart-number').innerText = record.chart_number;
        document.getElementById('symptoms-text').innerText = record.symptoms;
        document.getElementById('created-at').innerText = new Date(record.created_at).toLocaleString();
        const xrayImage = record.xray_images?.[0];
        document.getElementById('xray-img').src = xrayImage ? xrayImage.image_url : '';
        
        document.getElementById('predict-btn').onclick = () => this.handlePredict(patientId, recordId);
        document.getElementById('back-to-patient-btn').onclick = () => navigate(`/patients/${patientId}`);
        
        const analysisList = document.getElementById('analysis-list');
        if (analyses.length === 0) {
            analysisList.innerHTML = '<p>저장된 예측 결과가 없습니다.</p>';
        } else {
            analysisList.innerHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>수행 일시</th>
                            <th>폐렴 여부</th>
                            <th>Confidence</th>
                            <th>사용 모델</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${analyses.map(a => `
                            <tr class="${a.is_pneumonia ? 'result-positive' : 'result-negative'}">
                                <td>${new Date(a.created_at).toLocaleString()}</td>
                                <td><strong>${a.is_pneumonia ? 'Positive' : 'Negative'}</strong></td>
                                <td>${(a.confidence * 100).toFixed(2)}%</td>
                                <td>${a.ai_model}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }
    },

    async renderMyPage() {
        const html = await utils.loadTemplate('my-page');
        const app = document.getElementById('app');
        app.innerHTML = html;

        // 현재 사용자 정보 표시
        document.getElementById('me-email').innerText = state.user.email;
        document.getElementById('me-name-display').innerText = state.user.name;
        document.getElementById('me-department-display').innerText = state.user.department;
        document.getElementById('me-gender-display').innerText = state.user.gender === 'male' ? '남성' : '여성';
        document.getElementById('me-phone-display').innerText = utils.formatPhoneNumber(state.user.phone_number);
        document.getElementById('me-role-display').innerText = state.user.role;

        // 수정 폼 초기값 설정
        document.getElementById('update-me-department').value = state.user.department;
        document.getElementById('update-me-phone').value = utils.formatPhoneNumber(state.user.phone_number);
        
        const mePhoneInput = document.getElementById('update-me-phone');
        if (mePhoneInput) {
            mePhoneInput.addEventListener('input', (e) => utils.handlePhoneInput(e));
        }

        // 이벤트 바인딩
        document.getElementById('update-me-form').onsubmit = (e) => this.handleUpdateMe(e);
        document.getElementById('update-password-form').onsubmit = (e) => this.handleUpdatePassword(e);
        document.getElementById('delete-me-btn').onclick = () => this.handleDeleteMe();
    },

    async renderAdminUsers(params = {}) {
        const users = await apis.adminGetUsers(params);
        const html = await utils.loadTemplate('admin-users');
        if (state.currentPage !== '/admin/users') return;
        const app = document.getElementById('app');
        app.innerHTML = html;

        // 필드 값 복원
        const queryInput = document.getElementById('admin-search-query');
        const deptSelect = document.getElementById('admin-filter-dept');
        if (queryInput && params.query) queryInput.value = params.query;
        if (deptSelect && params.department) deptSelect.value = params.department;

        const listBody = document.getElementById('admin-users-list');
        if (users.length === 0) {
            listBody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem;">검색 결과가 없습니다.</td></tr>';
            return;
        }
        listBody.innerHTML = users.map(u => `
            <tr>
                <td>${u.id}</td>
                <td>${u.name}</td>
                <td>${u.email}</td>
                <td>${u.department}</td>
                <td>${utils.formatPhoneNumber(u.phone_number)}</td>
                <td>
                    <select onchange="pages.handleRoleUpdate(${u.id}, this.value)" ${u.id === state.user.id ? 'disabled' : ''}>
                        <option value="pending" ${u.role === 'pending' ? 'selected' : ''}>승인대기</option>
                        <option value="staff" ${u.role === 'staff' ? 'selected' : ''}>일반회원</option>
                        <option value="admin" ${u.role === 'admin' ? 'selected' : ''}>관리자</option>
                    </select>
                </td>
                <td>${u.is_active ? '<span class="status-badge success">활성</span>' : '<span class="status-badge error">비활성</span>'}</td>
            </tr>
        `).join('');
    },

    // --- Event Handlers ---

    handleAdminSearch() {
        const query = document.getElementById('admin-search-query').value;
        const department = document.getElementById('admin-filter-dept').value;
        
        const params = new URLSearchParams();
        if (query) params.set('query', query);
        if (department) params.set('department', department);
        
        const queryString = params.toString();
        const path = '/admin/users' + (queryString ? '?' + queryString : '');
        navigate(path);
    },

    resetAdminSearch() {
        navigate('/admin/users');
    },

    async handleRoleUpdate(userId, newRole) {
        try {
            await apis.adminUpdateUserRole({ user_id: userId, new_role: newRole });
            utils.showAlert('권한이 변경되었습니다.', 'success');
            this.handleAdminSearch();
        } catch (err) {
            utils.showAlert(`권한 변경 실패: ${err.message}`, 'error');
        }
    },

    async handleUpdateMe(e) {
        e.preventDefault();
        const data = {
            department: document.getElementById('update-me-department').value,
            phone_number: document.getElementById('update-me-phone').value.replace(/[^\d]/g, '')
        };

        try {
            await apis.updateMe(data);
            utils.showAlert('회원 정보가 수정되었습니다.', 'success');
            await checkAuth(); // state 갱신 (app.js)
            this.renderMyPage();
        } catch (err) {
            let msg = err.message;
            if (err.status === 500) msg = '잠시 후 다시시도해주세요.';
            utils.showAlert(msg, 'error', '수정 실패');
        }
    },

    async handleUpdatePassword(e) {
        e.preventDefault();
        const data = {
            current_password: document.getElementById('old-password').value,
            new_password: document.getElementById('new-password').value
        };

        try {
            await apis.updatePassword(data);
            utils.showAlert('비밀번호가 변경되었습니다.', 'success');
            e.target.reset();
        } catch (err) {
            let msg = err.message;
            if (err.status === 400) {
                msg = '비밀번호는 "대소문자, 특수문자, 숫자를 각 1개씩 포함한 8자리 이상이어야 합니다."';
            } else if (err.status === 500) {
                msg = '잠시 후 다시시도해주세요.';
            }
            utils.showAlert(msg, 'error', '비밀번호 변경 실패');
        }
    },

    async handleDeleteMe() {
        if (!confirm('정말로 탈퇴하시겠습니까? 모든 데이터가 삭제됩니다.')) return;

        try {
            await apis.deleteMe();
            utils.showAlert('탈퇴 처리가 완료되었습니다.', 'success');
            logout(); // (app.js)
        } catch (err) {
            utils.showAlert(`탈퇴 처리 실패: ${err.message}`, 'error');
        }
    },

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        await login(email, password); // (app.js)
    },

    async handleSignup(e) {
        e.preventDefault();
        const userData = {
            email: document.getElementById('signup-email').value,
            name: document.getElementById('signup-name').value,
            department: document.getElementById('signup-department').value,
            gender: document.getElementById('signup-gender').value,
            phone_number: document.getElementById('signup-phone').value.replace(/[^\d]/g, ''),
            password: document.getElementById('signup-password').value
        };

        try {
            await apis.signup(userData);
            utils.showAlert('회원가입이 완료되었습니다. 로그인해주세요.', 'success');
            navigate('/login');
        } catch (err) {
            let msg = err.message;
            if (err.status === 400 && (msg.includes('비밀번호') || msg.includes('password'))) {
                msg = '비밀번호는 "대소문자, 특수문자, 숫자를 각 1개씩 포함한 8자리 이상이어야 합니다."';
            }
            if (err.status === 500) msg = '잠시 후 다시시도해주세요.';
            utils.showAlert(msg, 'error', '가입 실패');
        }
    },

    async handlePatientCreate(e) {
        e.preventDefault();
        const patientData = {
            name: document.getElementById('name').value,
            age: parseInt(document.getElementById('age').value),
            gender: document.getElementById('gender').value,
            phone_number: document.getElementById('phone_number').value.replace(/[^\d]/g, '')
        };
        
        try {
            await apis.createPatient(patientData);
            utils.showAlert('환자가 등록되었습니다.', 'success');
            navigate('/patients');
        } catch (err) {
            utils.showAlert(`환자 등록 실패: ${err.message}`, 'error');
        }
    },

    handleSearch() {
        const name = document.getElementById('search-name').value;
        const gender = document.getElementById('filter-gender').value;
        const min_age = document.getElementById('filter-min-age').value;
        const max_age = document.getElementById('filter-max-age').value;

        const params = new URLSearchParams();
        if (name) params.set('name', name);
        if (gender) params.set('gender', gender);
        if (min_age) params.set('min_age', min_age);
        if (max_age) params.set('max_age', max_age);

        const queryString = params.toString();
        const path = '/patients' + (queryString ? '?' + queryString : '');
        navigate(path);
    },

    resetSearch() {
        navigate('/patients');
    },

    async handleRecordCreate(e, patientId) {
        e.preventDefault();
        const formData = new FormData();
        formData.append('patient_id', patientId);
        formData.append('chart_number', document.getElementById('chart_number').value);
        formData.append('symptoms', document.getElementById('symptoms').value);
        formData.append('xray_image', document.getElementById('xray_image').files[0]);

        try {
            await apis.createMedicalRecord(formData);
            utils.showAlert('진료 기록이 등록되었습니다.', 'success');
            navigate(`/patients/${patientId}`);
        } catch (err) {
            utils.showAlert(`진료 기록 등록 실패: ${err.message}`, 'error');
        }
    },

    openUpdateModal() {
        document.getElementById('update-modal').classList.add('show');
    },

    closeUpdateModal() {
        document.getElementById('update-modal').classList.remove('show');
    },

    async handlePatientUpdate(e) {
        e.preventDefault();
        const patientId = state.currentPatientId;
        const updateData = {
            name: document.getElementById('update-name').value,
            phone_number: document.getElementById('update-phone').value.replace(/[^\d]/g, '')
        };

        try {
            await apis.updatePatient(patientId, updateData);
            utils.showAlert('환자 정보가 수정되었습니다.', 'success');
            this.closeUpdateModal();
            this.renderPatientDetail(patientId);
        } catch (err) {
            utils.showAlert(`환자 정보 수정 실패: ${err.message}`, 'error');
        }
    },

    confirmDeletePatient() {
        document.getElementById('delete-modal').classList.add('show');
    },

    closeDeleteModal() {
        document.getElementById('delete-modal').classList.remove('show');
    },

    async handlePatientDelete() {
        const patientId = state.currentPatientId;
        try {
            await apis.deletePatient(patientId);
            utils.showAlert('환자 정보와 관련 데이터가 모두 삭제되었습니다.', 'success');
            this.closeDeleteModal();
            navigate('/patients');
        } catch (err) {
            utils.showAlert(`환자 삭제 실패: ${err.message}`, 'error');
        }
    },

    async handlePredict(patientId, recordId) {
        try {
            const prediction = await apis.predictPneumonia(
                patientId,
                recordId
            );
            if (!prediction) return;

            const resultText = prediction.is_pneumonia ? '폐렴' : '정상';
            const confidencePercent = (
                prediction.confidence * 100
            ).toFixed(2);

            utils.showAlert(
                `AI 예측 완료: ${resultText} (신뢰도 ${confidencePercent}%)`,
                'success'
            );

            navigate(`/patients/${patientId}/medical-records/${recordId}`, false);
        } catch (err) {
            const errorMessages = {
                403: 'AI 예측 기능을 사용할 권한이 없습니다.',
                404: '환자, 진료기록 또는 X-ray 파일을 찾을 수 없습니다.',
                503: 'AI 예측 모델을 현재 사용할 수 없습니다. 잠시 후 다시 시도해주세요.'
            };

            const message =
                errorMessages[err.status]
                || err.message
                || 'AI 예측 중 알 수 없는 오류가 발생했습니다.';

            utils.showAlert(`AI 예측 실패: ${message}`, 'error');
        }
    }
};
