const jwtDecode = require("jwt-decode");

export default function ({ redirect }) {
  let token = localStorage.getItem("token");
  if (token) {
    return redirect("/");
  }
}
