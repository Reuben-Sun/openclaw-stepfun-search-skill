#!/usr/bin/env python3
"""
StepFun Search Wrapper - StepFun API 网络搜索包装器
参考：amap-service (高德地图) 的结构化方法
"""

import sys
import json
import os
import requests
from typing import Optional, List, Dict

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

def stepfun_search(query: str, n: int = 5, category: str = "research") -> Optional[Dict]:
    """
    调用 StepFun 网络搜索 API
    
    Args:
        query: 搜索查询语句
        n: 返回结果数量（1-10）
        category: 搜索分类（research/programming/business/gov）
    
    Returns:
        dict: API 响应结果或 None（失败）
    """
    api_url = "https://api.stepfun.com/v1/search"
    api_key = os.getenv("STEPFUN_API_KEY")
    
    if not api_key:
        print("❌ Error: STEPFUN_API_KEY not set in environment", file=sys.stderr)
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    payload = {
        "query": query,
        "n": min(max(n, 1), 10),  # 限制在 1-10 之间
        "category": category if category in ["research", "programming", "business", "gov"] else "research"
    }
    
    try:
        print(f"🔍 Searching: {query} (category: {category}, results: {payload['n']})", file=sys.stderr)
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        results_count = len(result.get('results', []))
        print(f"✅ Found {results_count} results", file=sys.stderr)
        return result
    
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: Request took longer than 30 seconds", file=sys.stderr)
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}", file=sys.stderr)
        return None

def tavily_search(query: str, n: int = 5) -> Optional[Dict]:
    """
    调用 Tavily 搜索 API

    Args:
        query: 搜索查询语句
        n: 返回结果数量（1-10）

    Returns:
        dict: 与 StepFun 格式一致的搜索结果或 None（失败）
    """
    if TavilyClient is None:
        print("❌ Error: tavily-python is not installed. Run: pip install tavily-python", file=sys.stderr)
        return None

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        print("❌ Error: TAVILY_API_KEY not set in environment", file=sys.stderr)
        return None

    try:
        print(f"🔍 Searching (Tavily): {query} (results: {n})", file=sys.stderr)
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            max_results=min(max(n, 1), 10),
            search_depth="basic",
        )

        # Map Tavily results to the same shape as StepFun results
        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", ""),
                "source": "tavily",
            })

        print(f"✅ Found {len(results)} results (Tavily)", file=sys.stderr)
        return {"results": results}

    except Exception as e:
        print(f"❌ Tavily search error: {e}", file=sys.stderr)
        return None


def search(query: str, n: int = 5, category: str = "research") -> Optional[Dict]:
    """
    统一搜索入口：根据 SEARCH_PROVIDER 环境变量选择后端。
    支持 StepFun（默认）和 Tavily，并在 StepFun 失败时自动回退到 Tavily。

    Args:
        query: 搜索查询语句
        n: 返回结果数量（1-10）
        category: 搜索分类（仅 StepFun 使用）

    Returns:
        dict: 搜索结果或 None（失败）
    """
    provider = os.getenv("SEARCH_PROVIDER", "stepfun").lower()

    if provider == "tavily":
        return tavily_search(query, n)

    # Default: StepFun with Tavily fallback
    result = stepfun_search(query, n, category)
    if result is not None:
        return result

    # Fallback to Tavily on StepFun failure (e.g. 429 / 5xx)
    if os.getenv("TAVILY_API_KEY"):
        print("⚠️ StepFun failed, falling back to Tavily...", file=sys.stderr)
        return tavily_search(query, n)

    return None


def format_results_markdown(results: List[Dict]) -> str:
    """
    将搜索结果格式化为 Markdown（用于聊天展示）
    """
    if not results:
        return "❌ No results found"
    
    output = []
    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        url = result.get('url', '#')
        snippet = result.get('snippet', 'No snippet')
        source = result.get('source', 'Unknown')
        
        output.append(f"**{i}. {title}**")
        output.append(f"   🔗 {url} ({source})")
        output.append(f"   📝 {snippet}")
        output.append("")
    
    return "\n".join(output)

def format_results_text(results: List[Dict]) -> str:
    """
    将搜索结果格式化为纯文本
    """
    if not results:
        return "No results found"
    
    output = []
    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        url = result.get('url', 'N/A')
        snippet = result.get('snippet', 'N/A')
        source = result.get('source', 'Unknown')
        
        output.append(f"{i}. {title}")
        output.append(f"   Source: {source}")
        output.append(f"   URL: {url}")
        output.append(f"   {snippet}")
        output.append("")
    
    return "\n".join(output)

def main():
    """主函数：处理 CLI 参数"""
    if len(sys.argv) < 2:
        print("Usage: python stepfun_search.py '<query>' [n] [category] [format]")
        print("")
        print("Arguments:")
        print("  query    - Search keywords (必需)")
        print("  n        - Number of results (1-10, default: 5)")
        print("  category - Search category (research/programming/business/gov, default: research)")
        print("  format   - Output format (json/markdown/text, default: json)")
        print("")
        print("Examples:")
        print("  python stepfun_search.py 'Python asyncio'")
        print("  python stepfun_search.py 'Transformer attention' 5 research json")
        print("  python stepfun_search.py 'Python web framework' 5 programming markdown")
        sys.exit(1)
    
    query = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    category = sys.argv[3] if len(sys.argv) > 3 else "research"
    output_format = sys.argv[4] if len(sys.argv) > 4 else "json"
    
    # 执行搜索（通过统一入口，支持 StepFun / Tavily 切换与回退）
    result = search(query, n, category)
    if not result:
        print(json.dumps({"error": "Search failed"}, ensure_ascii=False))
        sys.exit(1)
    
    # 格式化输出
    results = result.get("results", [])
    
    if output_format == "markdown":
        print(format_results_markdown(results))
    elif output_format == "text":
        print(format_results_text(results))
    else:  # json (默认)
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
