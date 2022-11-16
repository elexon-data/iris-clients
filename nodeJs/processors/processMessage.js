import { mkdir, writeFile, stat } from "fs";
import { formatDateForFileName } from "../helpers/dateHelpers.js";
import path from "path";

const DATA_DIRECTORY = "data";

const args = process.argv.slice(2);
const consoleOnly = args.includes("--console-only");

const createFile = (dataset, content) => {
  const now = new Date();
  const fileName = `${dataset}_${formatDateForFileName(now)}.json`;
  const directory = path.join(DATA_DIRECTORY, dataset);
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

  if (consoleOnly) {
    console.log("Message body:", content);
  } else {
    createFile(dataset, content);
  }
};

export { processMessage };
