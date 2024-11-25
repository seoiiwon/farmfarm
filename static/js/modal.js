document.getElementById('cropSelect').addEventListener('change', function() {
    var selectedCropId = this.value;
    if (selectedCropId) {
        localStorage.setItem('selectedCropId', selectedCropId);
        window.location.href = `/${selectedCropId}`;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var selectElement = document.getElementById('cropSelect');
    var selectedCropId = localStorage.getItem('selectedCropId');

    if (selectedCropId) {
        var selectedOption = selectElement.querySelector(`option[value='${selectedCropId}']`);
        if (selectedOption) {
            selectedOption.selected = true;
            selectedOption.focus();
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
        status.addEventListener('click', (e) => {
            e.stopPropagation();

            const graphKey = status.getAttribute('data-graph-key');
            const statusValue = document.getElementById(`${status.id}Value`);
            const setData = statusValue.getAttribute('set-data');
            const curData = statusValue.getAttribute('cur-data');

            modal.style.display = 'flex';
            modalTitle.textContent = `${statusValue.textContent} 그래프`;
            desiredValue.textContent = setData;
            currentValue.textContent = curData;

            if (graphsData[graphKey]) {
                modalStatus.innerHTML = `
                    <img src="data:image/png;base64,${graphsData[graphKey]}" 
                         alt="${graphKey} graph" 
                         class="graphImage">
                `;
            } else {
                modalStatus.innerHTML = `<p>그래프를 불러올 수 없습니다.</p>`;
            }

            statusContainer.style.filter = 'blur(5px)';
        });
    });

    statusContainer.addEventListener('click', () => {
        modal.style.display = 'none';
        modalStatus.innerHTML = ""; 
        statusContainer.style.filter = 'none';
    });

    modal.addEventListener('click', (e) => {
        e.stopPropagation(); 
    });
});