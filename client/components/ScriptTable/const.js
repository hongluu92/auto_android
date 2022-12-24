export const columns = (context) => [

  {
    title: "Name",
    dataIndex: "name",
    key: "name",
    scopedSlots: { customRender: "name" },
  },
  {
    title: "Game",
    dataIndex: "game",
    key: "game",
    scopedSlots: { customRender: "game" },
  },
  {
    title: "Loop",
    dataIndex: "loop",
    key: "loop",
    scopedSlots: { customRender: "loop" },
  },
  {
    title: "Loop Delay" ,
    dataIndex: "loop_delay",
    key: "loop_delay",
    scopedSlots: { customRender: "loop_delay" }
  },
  {
    slots: { title: "actionTitle" },
    dataIndex: "action",
    key: "action",
    scopedSlots: { customRender: "action" },
    width: 145,
  },

];

 