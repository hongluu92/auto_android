export const DATE_FORMAT = "YYYY/MM/DD";
export const TIME_FORMAT = "HH:mm:ss";
export const DATE_TIME_FORMAT = `${DATE_FORMAT} ${TIME_FORMAT}`;
export const DATE_TIME_FORMAT_WITH_MS = `${DATE_TIME_FORMAT}.SSS`;
export const MODEL_STATUS = {
  COMPLETED: {
    label: "completed",
    color: "green",
  },
  PROCESSING: {
    label: "processing",
    color: "blue",
  },
  UPLOADED: {
    label: "uploaded",
    color: "goldenrod",
  },
  FAILED: {
    label: "failed",
    color: "red",
  },
  QUEUED_FOR_PROCESSING: {
    label: "queued",
    color: "goldenrod",
  },
  QUEUED_FOR_CONTINUE_PROCESSING: {
    label: "queued",
    color: "goldenrod",
  },
  QUEUED: {
    label: "queued",
    color: "goldenrod",
  },
  REMESHING: {
    label: "remeshing",
    color: "blue",
  },
  REMESHED: {
    label: "remeshed",
    color: "green",
  },
};
export const MODEL_TYPE = {
  IMAGE: {
    label: "image",
    color: "green",
  },
  VIDEO: {
    label: "video",
    color: "blue",
  },
};
