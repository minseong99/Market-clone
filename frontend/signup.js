const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");
  if (password1 === password2) return true;
  else return false;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  // {id:'asasg', password: "123"}
  // 암호화
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  const div = document.querySelector("#info");

  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    // data와 status값은 다른것임
    if (res.status === 200) {
      div.innerText = "회원가입에 성공했습니다.";
      div.style.color = "blue";
      //add
      alert("회원 가입에 성공했습니다.");
      window.location.pathname = "/login.html";
    }
  } else {
    div.innerText = "비밀번호가 같지 않습니다.";
    div.style.color = "red";
  }
};

const form = document.querySelector("#signup-form");
form.addEventListener("submit", handleSubmit);
