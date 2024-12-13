const navActions = {
    nav1: (cropId) => `/${cropId}`,
    nav2: (cropId) => `/status_all/${cropId}`,
    nav3: (cropId) => `/add_crop/${cropId}`,
};

const contentContainer = document.getElementById("content");

document.querySelectorAll(".navContent").forEach(nav => {
    nav.addEventListener("click", () => {
        const cropId = 1;

        // 현재 선택된 메뉴 저장
        localStorage.setItem("activeNav", nav.id);

        // URL 변경 및 페이지 새로고침
        const apiUrl = navActions[nav.id] ? (typeof navActions[nav.id] === 'function' ? navActions[nav.id](cropId) : navActions[nav.id]) : null;
        if (apiUrl) {
            window.location.href = apiUrl;
        }
    });
});

// DOMContentLoaded 이벤트에서 상태 복원
document.addEventListener("DOMContentLoaded", () => {
    const activeNav = localStorage.getItem("activeNav");
    document.querySelectorAll(".navContent").forEach(nav => {
        if (nav.id === activeNav) {
            nav.style.color = "#567D46";
            nav.style.fontWeight = "bold";
            nav.style.borderBottom = "3px solid black";
        } else {
            nav.style.color = "#A4A9A6";
            nav.style.fontWeight = "normal";
            nav.style.borderBottom = "none";
        }
    });
});

