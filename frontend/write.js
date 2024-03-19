const handleSubmitForm = async (event) => {
  // 제출은 순간적으로 되기 때문에 preventDefault메소드를 사용해야 한다.
  event.preventDefault();
  const body = new FormData(form);
  // form데이터 보낼때 세계시간 기준
  body.append("insertAt", new Date().getTime());
  try {
    const res = await fetch("/items", {
      method: "POST",
      body, // body:body
    });
    const data = await res.json();
    //글쓰기 성공(200)이면 페이지를 이동
    if (data == "200") window.location.pathname = "/"; // 루트 페이지로 이동
  } catch (e) {
    console.log.error(e);
  }
};

const form = document.getElementById("write-form");
form.addEventListener("submit", handleSubmitForm);
