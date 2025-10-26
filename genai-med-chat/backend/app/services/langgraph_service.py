# backend/app/services/langgraph_service.py
"""
LangGraphService

- If real `langgraph` SDK is installed, you can wire it here (optional).
- Otherwise this service will persist nodes/edges into MySQL via MySQLRepo.
- The idea: record reasoning steps as nodes (user message, retrieval hits, model output)
  and relations (e.g., user->retrieval, retrieval->generation).
"""

from typing import Dict, Any, Optional

try:
    import langgraph  # optional, if you want to use real LangGraph SDK
    HAS_LANGGRAPH = True
except Exception:
    HAS_LANGGRAPH = False

from app.repos.mysql_repo import MySQLRepo

class LangGraphService:
    def __init__(self):
        self.repo = MySQLRepo()
        self.use_langgraph = HAS_LANGGRAPH
        # If using real langgraph, initialize client here (left as optional)
        if self.use_langgraph:
            # Example placeholder; adapt to actual SDK usage if installed
            try:
                self.client = langgraph.Client()
            except Exception:
                self.client = None
                self.use_langgraph = False

    def record_node(self, conv_id: int, node_type: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Persist a node and return node_id. If langgraph is available, you could call its APIs instead.
        """
        if self.use_langgraph and self.client:
            # TODO: use langgraph client API
            # node_id = self.client.create_node(...)
            # return node_id
            pass
        # Fallback: write to MySQL graph_nodes
        node_id = self.repo.create_graph_node(conv_id=conv_id, node_type=node_type, content=content, metadata=metadata or {})
        return node_id

    def record_edge(self, conv_id: int, from_node: int, to_node: int, relation: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        if self.use_langgraph and self.client:
            # TODO: implement using langgraph client edge creation
            pass
        edge_id = self.repo.create_graph_edge(conv_id=conv_id, from_node=from_node, to_node=to_node, relation=relation, metadata=metadata or {})
        return edge_id

    def get_graph(self, conv_id: int):
        """
        Return nodes/edges (dict). If using langgraph, map/translate output.
        """
        if self.use_langgraph and self.client:
            # TODO: fetch from langgraph client and convert to dict
            pass
        return self.repo.get_graph(conv_id)
