import jwt_decode from "jwt-decode";
export default {
  computed: {
    currentUser() {
      let token = localStorage.getItem("token");
      if (token) {
        let decoded = jwt_decode(token);
        return decoded;
      }
    },
    isAdmin() {
      if (this.currentUser) {
        return this.currentUser.permissions.includes("admin");
      }
    },
    isUser() {
      if (this.currentUser) {
        return this.currentUser.permissions.includes("user");
      }
    },
    isMobile() {
      let isMobile = window.matchMedia(
        "only screen and (max-width: 767px)"
      ).matches;
      return isMobile;
    },
  },
  methods: {
    checkIfDeviceHasTouchScreen(file) {
      var hasTouchScreen = false;

      if ("maxTouchPoints" in navigator) {
        hasTouchScreen = navigator.maxTouchPoints > 0;
      } else if ("msMaxTouchPoints" in navigator) {
        hasTouchScreen = navigator.msMaxTouchPoints > 0;
      } else {
        var mQ = window.matchMedia && matchMedia("(pointer:coarse)");
        if (mQ && mQ.media === "(pointer:coarse)") {
          hasTouchScreen = !!mQ.matches;
        } else if ("orientation" in window) {
          hasTouchScreen = true; // deprecated, but good fallback
        } else {
          // Only as a last resort, fall back to user agent sniffing
          var UA = navigator.userAgent;
          hasTouchScreen =
            /\b(BlackBerry|webOS|iPhone|IEMobile)\b/i.test(UA) ||
            /\b(Android|Windows Phone|iPad|iPod)\b/i.test(UA);
        }
      }

      this.hasTouchScreen = hasTouchScreen;
    },
  },
};
