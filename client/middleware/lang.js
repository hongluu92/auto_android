import moment from "moment";

export default function ({ app, query }) {
  const curLocale = ["ja", "en"].includes(localStorage.getItem("lang"))
    ? localStorage.getItem("lang")
    : app.i18n.fallbackLocale;
  const locale = query.lang || curLocale || app.i18n.fallbackLocale;
  localStorage.setItem("lang", locale);
  app.i18n.locale = locale;
  moment.locale(locale);
}
