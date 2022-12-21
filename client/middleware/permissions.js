import jwtDecode from "jwt-decode";
const _ = require("lodash");

export default function ({ route, redirect }) {
  return True
  let token = localStorage.getItem("token");
  let decoded = jwtDecode(token);
  let userPermissions = decoded.permissions;

  let { meta } = route;
  const permissions =
    meta.length && meta[0].permissions ? _.cloneDeep(meta[0].permissions) : -1;
  // Validate role of user, if in list role of user contain => pass
  if (permissions !== -1) {
    let hasPermission = false;
    let equals = _.filter(permissions, (item) => {
      return _.findIndex(userPermissions, (o) => o == item) >= 0;
    });
    if (equals.length > 0) hasPermission = true;

    if (!hasPermission) {
      return redirect("/not-authorized");
    }
  }
}
