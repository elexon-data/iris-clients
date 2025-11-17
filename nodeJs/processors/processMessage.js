import { mkdir, writeFile, stat } from "fs";
import { formatDateForFileName } from "../helpers/dateHelpers.js";
import path from "path";
import config from "../config.js";

const createFile = (dataset, fileName, content) => {
  const directory = path.join(config.downloadDirectory, dataset);
  const filePath = path.join(directory, fileName);

  stat(directory, (err) => {
    // Create directory if it doesn't already exist
    if (err) {
      console.log(`Creating directory "${directory}"`);
      mkdir(directory, { recursive: true }, () => {
        console.log(`Created directory "${directory}"`);
      });
    }

    writeFile(filePath, content, () => {
      console.log(`Created file "${fileName}"`);
    });
  });
};

const processMessage = async (messageReceived) => {
  const now = new Date();
  const dataset = messageReceived.subject ?? "unknown";
  const fileName = messageReceived.messageId ?? `${dataset}_${formatDateForFileName(now)}.json`;

  const body = JSON.parse(messageReceived.body);

  const content = JSON.stringify(body, null, 2);
  createFile(dataset, fileName, content);
};

export { processMessage };
