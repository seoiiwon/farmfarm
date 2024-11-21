document.getElementById('cropSelect').addEventListener('change', function() {
    var selectedCropId = this.value;
    if (selectedCropId) {
        // 선택된 값 저장
        localStorage.setItem('selectedCropId', selectedCropId);
        window.location.href = `/${selectedCropId}`;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var selectElement = document.getElementById('cropSelect');
    var selectedCropId = localStorage.getItem('selectedCropId');  // 저장된 선택값 읽기

    if (selectedCropId) {
        // 선택된 값에 해당하는 옵션을 찾고 포커스 맞추기
        var selectedOption = selectElement.querySelector(`option[value='${selectedCropId}']`);
        if (selectedOption) {
            selectedOption.selected = true;
            selectedOption.focus();  // 선택된 옵션에 포커스 맞추기
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {

    const statuses = document.querySelectorAll('.status');
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modalTitle');
    const modalStatus = document.getElementById('modalStatus');
    const statusContainer = document.getElementById('statusContainer');

    const desiredValue = document.getElementById('desiredValue');
    const currentValue = document.getElementById('currentValue');

    statuses.forEach(status => {
        status.addEventListener('click', () => {
            const id = status.id; // status1, status2, ...
            const statusValue = document.getElementById(`${id}Value`);
            const setData = statusValue.getAttribute('set-data');
            const curData = statusValue.getAttribute('cur-data');

            // 모달 표시
            modal.style.display = 'flex';
            modalTitle.textContent = `상태: ${statusValue.textContent}`;
            modalStatus.textContent = `상태 상세`;

            // 모달에 값 설정
            desiredValue.textContent = setData;
            currentValue.textContent = curData;

            // 배경 흐리게
            statusContainer.style.filter = 'blur(5px)';
        });
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            statusContainer.style.filter = 'none';
        }
    });
});