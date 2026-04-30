# Data Model: 001-bookmarks-manager

## Core Entities

```python
@dataclass
class Bookmark:
    title: str
    url: str
    add_date: Optional[datetime] = None
    icon: Optional[str] = None
    folder: str = "root"
    theme: Optional[str] = None

@dataclass
class Theme:
    name: str
    emoji: str
    agent_id: int

@dataclass
class BookmarkCollection:
    bookmarks: List[Bookmark]
    themes: List[Theme]
    metadata: CollectionMetadata

@dataclass
class CollectionMetadata:
    source_file: str
    import_date: datetime
    total_count: int
    categorized_count: int
```

## State (LangGraph)

```python
@dataclass
class GraphState:
    bookmarks: List[Bookmark]
    themes: List[Theme]
    unprocessed: List[Bookmark]
    assignments: Dict[str, str]  # bookmark_url -> theme_name
    errors: List[str]
```

## CLI Arguments

```python
@click.group()
def cli():
    pass

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--max-themes", default=10, help="Max theme categories")
@click.option("--output", "-o", type=click.Path(), help="Output file")
def import_bookmarks(input_file, max_themes, output):
    pass

@cli.command()
@click.argument("query")
@click.option("--limit", default=10, help="Max results")
def search(query, limit):
    pass
```