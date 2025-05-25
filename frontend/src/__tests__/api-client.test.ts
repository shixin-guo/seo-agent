/**
 * Tests for the API client.
 *
 * Note: This is a placeholder for actual tests. In a real implementation,
 * you would use Jest or another testing framework to run these tests.
 */

import {
  generateKeywords,
  optimizeContent,
  auditSite,
  analyzeBacklinks,
  checkApiStatus,
} from "../lib/api/api-client";

// Mock fetch to avoid actual API calls
global.fetch = jest.fn();

describe("API Client", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  describe("generateKeywords", () => {
    it("should call the keywords API with the correct parameters", async () => {
      // Arrange
      const mockResponse = {
        json: jest.fn().mockResolvedValue({ keywords: [] }),
        ok: true,
      };
      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      // Act
      await generateKeywords("seo", "technology");

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/api/keywords"),
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
          }),
          body: JSON.stringify({ seed: "seo", industry: "technology" }),
        }),
      );
    });
  });

  describe("optimizeContent", () => {
    it("should call the optimize-content API with the correct parameters", async () => {
      // Arrange
      const mockResponse = {
        json: jest.fn().mockResolvedValue({}),
        ok: true,
      };
      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      const contentFile = new File(["content"], "content.txt");
      const formData = new FormData();
      formData.append("content_file", contentFile);
      formData.append("use_advanced", "true");
      formData.append("creative", "false");

      // Act
      await optimizeContent(contentFile);

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/api/optimize-content"),
        expect.objectContaining({
          method: "POST",
          body: expect.any(FormData),
        }),
      );
    });
  });

  describe("auditSite", () => {
    it("should call the audit-site API with the correct parameters", async () => {
      // Arrange
      const mockResponse = {
        json: jest.fn().mockResolvedValue({}),
        ok: true,
      };
      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      // Act
      await auditSite("example.com", 50);

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/api/audit-site"),
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
          }),
          body: JSON.stringify({ domain: "example.com", max_pages: 50 }),
        }),
      );
    });
  });

  describe("analyzeBacklinks", () => {
    it("should call the backlink-analysis API with the correct parameters", async () => {
      // Arrange
      const mockResponse = {
        json: jest.fn().mockResolvedValue({}),
        ok: true,
      };
      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      // Act
      await analyzeBacklinks("example.com", ["competitor1.com"], true);

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/api/backlink-analysis"),
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
          }),
          body: JSON.stringify({
            domain: "example.com",
            competitors: ["competitor1.com"],
            generate_templates: true,
          }),
        }),
      );
    });
  });

  describe("checkApiStatus", () => {
    it("should call the root API endpoint", async () => {
      // Arrange
      const mockResponse = {
        ok: true,
      };
      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      // Act
      const result = await checkApiStatus();

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining("/"));
      expect(result).toBe(true);
    });

    it("should return false if the API is not available", async () => {
      // Arrange
      (global.fetch as jest.Mock).mockRejectedValue(new Error("Network error"));

      // Act
      const result = await checkApiStatus();

      // Assert
      expect(result).toBe(false);
    });
  });
});
