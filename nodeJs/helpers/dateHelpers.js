/**
 * Formats a datetime to be used as part of a filename
 * @param {Date} date The date to be formatted
 * @returns {string} The datetime in the format yyyy-MM-ddTHH-mm-ss_SSS
 */
const formatDateForFileName = (date) =>
  date.toISOString().slice(null, 23).replaceAll(":", "-").replaceAll(".", "_");

export { formatDateForFileName };
