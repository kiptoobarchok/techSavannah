import type { NextConfig } from "next";
import { loadEnvConfig } from "@next/env";
import path from "path";

loadEnvConfig(path.resolve(process.cwd(), ".."));

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
