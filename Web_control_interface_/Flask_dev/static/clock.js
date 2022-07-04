
            const clock = document.getElementById("clock");
            function msg_send(){
                document.message_form.submit()
            }

            function getClock(){
                const date = new Date()
                const year = String(date.getFullYear()).padStart(2,"0");
                const month = String(date.getMonth()).padStart(2,"0");
                const day = String(date.getDate()).padStart(2,"0");
                const hour = String(date.getHours()).padStart(2,"0");
                const minutes = String(date.getMinutes()).padStart(2,"0");
                const second = String(date.getSeconds()).padStart(2,"0");//number이기 때문에 padStart 붙일 수 없음. String 변환해주어야한다.
                clock.innerText = `${year}-${month}-${day} ${hour}:${minutes}:${second}`;
                }
            getClock();
            setInterval(getClock, 1000);