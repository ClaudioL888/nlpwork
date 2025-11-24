from __future__ import annotations

from collections import Counter


def build_sentiment_graph(quotes: list[dict]) -> dict:
    nodes = []
    edges = []
    counter = Counter(quote["label"] for quote in quotes if quote.get("label"))
    for label, count in counter.items():
        nodes.append({"id": label, "label": label, "size": count})
    if len(nodes) >= 2:
        labels = [node["id"] for node in nodes]
        for idx, src in enumerate(labels):
            for dst in labels[idx + 1 :]:
                edges.append({"source": src, "target": dst, "weight": 1})
    return {"nodes": nodes, "edges": edges}
