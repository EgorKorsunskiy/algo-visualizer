import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  turbopack: {
    rules: {
      "*.glsl": {
        loaders: ['raw-loader'],
        as: "*.ts"
      }
    }
  }
};

export default nextConfig;
