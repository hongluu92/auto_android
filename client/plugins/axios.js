export default function ({ $axios, redirect }) {
  $axios.interceptors.request.use((config) => {
    let token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = "Bearer " + token;
    }
    return config;
  });

  $axios.setHeader("Content-Type", "application/json", ["post", "put"]);

  $axios.onError((error) => {
    const code = parseInt(error.response && error.response.status);
    if (code === 401) {
      localStorage.clear();
      redirect("/login");
    }
  });
}
