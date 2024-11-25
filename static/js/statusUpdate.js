document.getElementById("settingValue").addEventListener("submit", async function (event) {
    event.preventDefault();
    
    const setTemperature = document.getElementById("setting1Value").value;
    const setHumidity = document.getElementById("setting2Value").value;
    const setSolidHumidity = document.getElementById("setting3Value").value;
    const setIlluminance = document.getElementById("setting4Value").value;
    const setCo2Concentration = document.getElementById("setting5Value").value;
    const setWaterTemperature = document.getElementById("setting6Value").value;

    const cropId = window.location.pathname.split("/")[2];

    const apiUrl = `/update_status/${cropId}`;

    try {
        const response = await fetch(apiUrl, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                set_temperature: setTemperature,
                set_humidity: setHumidity,
                set_solidHumidity: setSolidHumidity,
                set_illuminance: setIlluminance,
                set_co2Concentration: setCo2Concentration,
                set_waterTemperature: setWaterTemperature,
            }),
        });

        if (!response.ok) {
            throw new Error(`API 요청 실패 - 상태 코드: ${response.status}`);
        }

        const data = await response.json();

        alert("설정이 성공적으로 업데이트 되었습니다!");
        console.log(data);
    } catch (error) {
        console.error("API 호출 중 오류:", error);
        alert("설정 업데이트 중 오류가 발생했습니다.");
    }
});