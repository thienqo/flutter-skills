window.onload = function () {
  const ui = SwaggerUIBundle({
    spec: {
      "openapi": "3.0.3",
      "info": {"title": "Embedded Neutral API", "version": "1.0.0"},
      "paths": {
        "/status": {
          "get": {
            "operationId": "getStatus",
            "responses": {"200": {"description": "OK"}}
          }
        }
      }
    },
    dom_id: "#swagger-ui"
  });
  window.ui = ui;
};
