const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  // {id:'asasg', password: "123"}
  // 암호화
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();

  accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);

  alert("로그인 되었습니다.");

  window.location.pathname = "/";
};

let accessToken = null;

const form = document.querySelector("#login-form");
form.addEventListener("submit", handleSubmit);
