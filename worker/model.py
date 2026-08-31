from PIL import Image
from torchvision import transforms
from pathlib import Path

import torch
from torch import nn


class SimpleCNN(nn.Module):
    """
    흉부 X-ray 이미지를 두 개 클래스로 분류하는 CNN 모델입니다.

    입력 형태:
        [이미지 개수, 채널 수, 높이, 너비]

    출력 형태:
        이미지마다 두 클래스의 점수(logits)를 반환합니다.
        각 클래스가 무엇을 의미하는지는 학습 당시 클래스 순서를
        확인한 후 예측 함수에서 연결합니다.
    """

    def __init__(self) -> None:
        super().__init__()

        # [1단계] 이미지의 특징을 추출합니다.
        #
        # Conv2d:
        # 이미지의 선, 모양 같은 특징을 찾습니다.
        #
        # ReLU:
        # 모델이 복잡한 특징을 학습할 수 있도록 값을 변환합니다.
        #
        # MaxPool2d:
        # 이미지 크기를 절반으로 줄여 중요한 특징만 남깁니다.
        self.conv = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=16,
                kernel_size=3,
                stride=1,
                padding=1,
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(
                in_channels=16,
                out_channels=32,
                kernel_size=3,
                stride=1,
                padding=1,
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        # [2단계] 추출된 특징을 두 개 클래스의 점수로 변환합니다.
        #
        # Flatten:
        # 여러 차원으로 된 특징을 한 줄로 펼칩니다.
        #
        # Linear:
        # 32,768개의 특징을 두 개 클래스 점수로 변환합니다.
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 32 * 32, 2),
        )

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        """입력 이미지에서 특징을 추출하고 분류 점수를 반환합니다."""
        features = self.conv(image)
        return self.fc(features)


# 현재 파일을 기준으로 모델 가중치의 절대 경로를 만듭니다.
# 실행 위치가 달라져도 동일한 모델 파일을 찾을 수 있습니다.
MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "model_state_dict.pth"
)


def select_device() -> torch.device:
    """
    현재 컴퓨터에서 사용할 수 있는 가장 적절한 연산 장치를 선택합니다.

    Windows의 NVIDIA GPU는 CUDA, Apple Silicon Mac은 MPS를 사용하며,
    두 장치를 사용할 수 없으면 모든 컴퓨터에서 지원되는 CPU를 사용합니다.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")

    if (
        hasattr(torch.backends, "mps")
        and torch.backends.mps.is_available()
    ):
        return torch.device("mps")

    return torch.device("cpu")


def load_model() -> tuple[SimpleCNN, torch.device]:
    """
    모델 구조를 만든 뒤 학습된 가중치를 적용해 메모리에 올립니다.

    가중치는 CPU로 먼저 읽기 때문에 CUDA에서 저장된 파일도
    Mac과 CPU 환경에서 안전하게 불러올 수 있습니다.
    """
    device = select_device()
    model = SimpleCNN()

    # weights_only=True는 실행 코드가 아닌 가중치만 불러오는 옵션입니다.
    state_dict = torch.load(
        MODEL_PATH,
        map_location="cpu",
        weights_only=True,
    )
    model.load_state_dict(state_dict)

    # 선택한 연산 장치로 모델을 이동합니다.
    model.to(device)

    # Dropout, BatchNorm 등이 예측 방식으로 동작하도록 설정합니다.
    model.eval()

    return model, device


# worker.model을 처음 import할 때 모델을 한 번만 메모리에 올립니다.
# 이후 예측 요청에서는 같은 MODEL을 재사용합니다.
MODEL, DEVICE = load_model()

# [3. X-ray 이미지 전처리]
# 모델이 학습할 때 사용한 형태와 동일하게 이미지를 변환합니다.
IMAGE_TRANSFORM = transforms.Compose(
    [
        # 컬러 이미지가 들어와도 흑백 1채널로 변환합니다.
        transforms.Grayscale(num_output_channels=1),

        # 모델의 입력 크기인 128×128로 맞춥니다.
        transforms.Resize((128, 128)),

        # 이미지를 PyTorch가 계산할 수 있는 숫자 배열로 변환합니다.
        # 픽셀값은 0~255에서 0.0~1.0 범위로 바뀝니다.
        transforms.ToTensor(),
    ]
)


def preprocess_image(image_path: str | Path) -> torch.Tensor:
    """X-ray 이미지 파일을 모델이 입력받을 수 있는 형태로 변환합니다."""

    # with 문을 사용하면 이미지 처리가 끝난 뒤 파일이 자동으로 닫힙니다.
    with Image.open(image_path) as image:
        image_tensor = IMAGE_TRANSFORM(image)

    # 변환 직후 모양: [채널, 높이, 너비] = [1, 128, 128]
    # 모델은 여러 이미지를 한 번에 받는 형태를 요구하므로
    # 맨 앞에 배치 크기(이미지 개수) 차원을 추가합니다.
    image_tensor = image_tensor.unsqueeze(0)

    # 최종 모양: [배치, 채널, 높이, 너비] = [1, 1, 128, 128]
    # 모델과 입력 이미지가 같은 연산 장치에서 계산되도록 이동합니다.
    return image_tensor.to(DEVICE)

# 모델 출력 번호와 실제 클래스 이름의 대응 관계입니다.
# 0번은 정상, 1번은 폐렴으로 해석합니다.
MODEL_NAME = "SimpleCNN"
CLASS_NAMES = ("NORMAL", "PNEUMONIA")


def predict_pneumonia(image_path: str | Path) -> dict[str, int | str | bool | float]:
    """X-ray 이미지를 분석하여 정상 또는 폐렴 예측 결과를 반환합니다."""

    # 1. 이미지 파일을 모델 입력 형태로 변환합니다.
    image_tensor = preprocess_image(image_path)

    # 2. 예측할 때는 학습에 필요한 기울기 계산을 하지 않습니다.
    # 메모리 사용량이 줄고 예측 속도가 빨라집니다.
    with torch.inference_mode():
        logits = MODEL(image_tensor)

        # 모델의 원시 출력값을 0~1 사이의 확률로 변환합니다.
        probabilities = torch.softmax(logits, dim=1)[0]

    # 가장 확률이 높은 클래스 번호를 최종 예측으로 선택합니다.
    predicted_class = int(torch.argmax(probabilities).item())

    normal_probability = float(probabilities[0].item())
    pneumonia_probability = float(probabilities[1].item())
    confidence = float(probabilities[predicted_class].item())

    # API 응답에 바로 사용할 수 있도록 딕셔너리 형태로 반환합니다.
    return {
        "class_id": predicted_class,
        "label": CLASS_NAMES[predicted_class],
        "is_pneumonia": predicted_class == 1,
        "confidence": round(confidence, 6),
        "normal_probability": round(normal_probability, 6),
        "pneumonia_probability": round(pneumonia_probability, 6),
    }