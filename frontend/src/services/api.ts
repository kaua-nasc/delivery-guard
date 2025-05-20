import axios from "axios";

export const instance = axios.create({
  baseURL: "https://localhost:3000",
  timeout: 5000
});
