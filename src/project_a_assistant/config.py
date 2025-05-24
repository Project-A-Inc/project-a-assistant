from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

from pydantic import Field, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        case_sensitive=False,
        extra="ignore"
    )

    # FastMCP (optional)
    mcp_base_url: str | None = Field(None, alias="MCP_BASE_URL")
    mcp_api_key: str        | None = Field(None, alias="MCP_API_KEY")
    mcp_api_header: str        | None = Field(None, alias="MCP_API_HEADER")
    

    # Azure OpenAI
    azure_endpoint: AnyHttpUrl = Field(..., alias="AZURE_OPENAI_ENDPOINT")
    azure_key: str             = Field(..., alias="AZURE_OPENAI_API_KEY")
    azure_deployment: str      = Field(..., alias="AZURE_OPENAI_DEPLOYMENT_NAME")

    # Model params
    llm_temperature: float = Field(0.2, alias="LLM_TEMPERATURE")
    llm_max_tokens:    int = Field(1024, alias="LLM_MAX_TOKENS")
    llm_top_p:        float = Field(1.0, alias="LLM_TOP_P")

    # Storage params

    azure_storage_connection_string: str = Field(..., alias="AZURE_STORAGE_CONNECTION_STRING")
    blob_container: str             = Field(..., alias="BLOB_CONTAINER")
    
    # Org params
    default_user_id: str             = Field(..., alias="DEFAULT_USER_ID")
    default_org_id: str      = Field(..., alias="DEFAULT_ORG_ID")


    @field_validator("mcp_base_url", "mcp_api_key", mode="before")
    def _empty_str_to_none(cls, v):
        
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @property
    def has_mcp(self) -> bool:
        return bool(self.mcp_base_url and self.mcp_api_key)

@lru_cache()
def get_settings() -> Settings:
    return Settings()
