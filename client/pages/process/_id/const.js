export const columns = [
  {
    title: "Config name",
    dataIndex: "name",
    key: "name",
    scopedSlots: { customRender: "configName" },
  },
  {
    title: "Status",
    dataIndex: "status",
    key: "status",
    scopedSlots: { customRender: "status" },
  },
];
