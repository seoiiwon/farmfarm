document.getElementById('cropForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries()); // Convert form data to JSON-like object

    // Make a POST request to FastAPI
    try {
        const response = await fetch('/create_new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data), // Send form data as JSON
        });

        if (response.ok) {
            alert('작물이 성공적으로 등록되었습니다!');
        } else {
            alert('등록 실패. 다시 시도해 주세요.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('서버와의 연결에 문제가 발생했습니다.');
    }
});
