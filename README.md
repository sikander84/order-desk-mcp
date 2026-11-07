# Order Desk MCP

An AI-powered order management application built using Python, FastAPI, and Model Context Protocol (MCP).

The project demonstrates how AI assistants can interact with an order management system through MCP tools, enabling users to retrieve order information and perform order-related operations using natural language.

## Project Objectives

- Build a REST API using FastAPI.
- Develop an MCP server to expose order management capabilities to AI assistants.
- Implement tools for retrieving and managing customer orders.
- Use Pydantic for data validation and structured responses.
- Write automated tests using Pytest.

## Technology Stack

- **Python** – Core programming language
- **uv** – Python package and dependency management
- **FastAPI** – REST API framework
- **Uvicorn** – ASGI application server
- **MCP** – Model Context Protocol integration
- **Pydantic** – Data validation and models
- **HTTPX** – HTTP client
- **Pytest** – Automated testing
- **Git/GitHub** – Version control

## Project Structure

order-desk-mcp/
├── data/orders.json           # 6 fake orders, one per case
├── src/order_desk/
│   ├── models.py              # pydantic: raw API shapes + clean tool outputs
│   ├── mock_api.py            # FastAPI order API
│   ├── mapping.py             # nested payload -> OrderSummary
│   ├── returns.py             # return eligibility rules
│   ├── client.py              # HTTP client with retries
│   ├── service.py             # tool logic + customer verification
│   └── server.py              # MCP server (3 tools)
├── tests/                     # conftest + one test file per module
├── .github/workflows/ci.yml
├── CLAUDE.md
└── README.md


### Running the Application

Application startup instructions will be added as the FastAPI and MCP server components are implemented.


## Development Roadmap

- [ ] Set up the Python project structure.
- [ ] Implement order data models using Pydantic.
- [ ] Build REST API endpoints using FastAPI.
- [ ] Implement MCP server and order management tools.
- [ ] Integrate MCP tools with the order management API.
- [ ] Add automated tests.
- [ ] Document setup and usage instructions.
