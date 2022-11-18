import { mkdir, writeFile, stat } from "fs";
import { formatDateForFileName } from "../helpers/dateHelpers.js";
import path from "path";
import config from "../config.js";

const createFile = (dataset, content) => {
  const now = new Date();
  const fileName = `${dataset}_${formatDateForFileName(now)}.json`;
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

    console.log(`Creating file "${fileName}"`);
    writeFile(filePath, content, () => {
      console.log(`Created file "${fileName}"`);
    });
  });
};

const processMessage = async (messageReceived) => {
  console.log("Processing message");

  const body = JSON.parse(messageReceived.body);
  const dataset = body?.[0]?.dataset;

  if (!dataset) {
    throw new Error("Unable to find dataset in message");
  }

  const content = JSON.stringify(body, null, 2);
  createFile(dataset, content);
};

export { processMessage };
