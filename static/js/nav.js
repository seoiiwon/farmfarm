const navActions = {
    nav1: "/",
    nav2: "/status_all",
    nav3: "/add_crop"
};

const contentContainer = document.getElementById("content");

document.querySelectorAll(".navContent").forEach(nav => {
    nav.addEventListener("click", async () => {
        const apiUrl = navActions[nav.id]; // 버튼 ID에 따라 API URL 선택
        if (!apiUrl) return;

        try {
            // API 호출
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error("API 요청 실패");
            }
            
            // HTML 콘텐츠 로드
            const parser = new DOMParser();
            const htmlDoc = parser.parseFromString(await response.text(), "text/html");
            const newContent = htmlDoc.querySelector("main#content"); // main 태그 추출

            if (newContent) {
                contentContainer.innerHTML = newContent.innerHTML; // 콘텐츠 교체
                // URL 변경 (브라우저 히스토리 업데이트)
                window.history.pushState({}, "", apiUrl);
            } else {
                throw new Error("HTML 구조가 올바르지 않습니다.");
            }
        } catch (error) {
            console.error("API 호출 중 오류:", error);
            contentContainer.innerHTML = "콘텐츠 로드 에러";
        }
    });
});