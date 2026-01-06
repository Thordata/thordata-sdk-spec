package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
)

// Simplified response structures
type Response struct {
	Code int    `json:"code"`
	Msg  string `json:"msg,omitempty"`
	Data any    `json:"data,omitempty"`
}

func main() {
	r := gin.Default()

	// 1. Scraper API (SERP)
	// POST /request
	r.POST("/request", func(c *gin.Context) {
		// Detect if SERP or Universal based on params or header?
		// For simplicity, we assume if engine param exists -> SERP, else Universal
		engine := c.PostForm("engine")
		urlVal := c.PostForm("url")

		if engine != "" {
			// SERP Response
			c.JSON(200, gin.H{
				"code":    200,
				"organic": []gin.H{{"title": "Mock Result", "link": "http://mock.com"}},
				"engine":  engine,
			})
			return
		} else if urlVal != "" {
			// Universal Response
			format := c.PostForm("type")
			if format == "png" {
				// 1x1 pixel base64
				c.JSON(200, gin.H{
					"code": 200,
					"png":  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMB/6Xn2mQAAAAASUVORK5CYII=",
				})
			} else {
				c.JSON(200, gin.H{
					"code": 200,
					"html": "<html><body>Mock Content</body></html>",
				})
			}
			return
		}
		c.JSON(400, Response{Code: 400, Msg: "Missing engine or url"})
	})

	// 2. Web Scraper API (Tasks)
	r.POST("/builder", func(c *gin.Context) {
		c.JSON(200, Response{Code: 200, Data: gin.H{"task_id": "mock_task_123"}})
	})
	r.POST("/video_builder", func(c *gin.Context) {
		c.JSON(200, Response{Code: 200, Data: gin.H{"task_id": "mock_vid_123"}})
	})
	r.POST("/tasks-status", func(c *gin.Context) {
		// Mock logic: returns "ready"
		c.JSON(200, Response{Code: 200, Data: []gin.H{
			{"task_id": "mock_task_123", "status": "ready"},
		}})
	})
	r.POST("/tasks-download", func(c *gin.Context) {
		c.JSON(200, Response{Code: 200, Data: gin.H{"download": "http://mock.com/data.json"}})
	})

	// 3. Public API (Account)
	r.GET("/account/usage-statistics", func(c *gin.Context) {
		c.JSON(200, Response{Code: 200, Data: gin.H{
			"total_usage_traffic": 1024 * 1024 * 100, // 100MB
			"traffic_balance":     1024 * 1024 * 500, // 500MB
		}})
	})

	// 4. Proxy API
	r.GET("/proxy/proxy-list", func(c *gin.Context) {
		c.JSON(200, Response{Code: 200, Data: []gin.H{
			{"ip": "1.2.3.4", "port": 8888, "username": "u", "password": "p"},
		}})
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("Mock server listening on %s", port)
	r.Run(":" + port)
}
