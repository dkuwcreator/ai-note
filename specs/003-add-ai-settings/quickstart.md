# Quickstart: In-app AI Settings & Rewrite Modes

## Configuring AI Connection

1. Open the application.
2. Navigate to `Settings` from the main menu.
3. Select the `Connection` tab.
4. Fill in the following fields:
   - **Endpoint**: Your Azure OpenAI endpoint.
   - **Deployment ID**: The deployment identifier.
   - **API Version** (optional): Specify if required.
   - **Timeout** (optional): Default is 6 seconds.
   - **Retry Preferences** (optional): Configure retries if needed.
5. Paste your API key into the `API Key` field.
6. Click `Test Connection` to validate the settings.
7. Save the settings.

## Managing Rewrite Modes

1. Open `Settings` and select the `Rewrite Modes` tab.
2. To create a new mode:
   - Click `Add New`.
   - Enter a name and instruction template.
   - Choose `Applies To` (selection-only or whole-note-default).
   - (Optional) Expand `Advanced Settings` to configure additional fields.
   - Click `Save`.
3. To edit an existing mode:
   - Select the mode from the list.
   - Modify the fields and click `Save`.
4. To reorder modes:
   - Use the `Move Up` / `Move Down` buttons to adjust display order.
5. To enable/disable a mode:
   - Toggle the `Enabled` switch.
6. To delete a mode:
   - Select the mode and click `Delete`.

## Security Guidance

- API keys are stored securely using the OS keyring when available. If the OS keyring is not available, the Settings dialog offers an encrypted local fallback protected by a user-provided passphrase.
- If using local storage, ensure you remember the passphrase — lost passphrases cannot be recovered.
- Never commit secrets to source control.

## Example `.env` Template

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://example.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=my-deployment
AZURE_OPENAI_API_KEY=your-api-key
```

## Gitignore Snippet

```gitignore
# Exclude local secrets storage
*.secrets
```