# Cursor Configuration User Rules

In Cursor Settings, modify Rules by copying the content of Cursor_User_Rules_EN.md file into Rules.
![image-20250629192245458](./assets/image-20250629192245458.png)

**Note**: The User Rules I provide are for general project development, so they include the MCP tool `playwright` for UI testing. If you're developing projects that include UI, add this tool as shown in the example below:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ]
    }
  }
}
``` 