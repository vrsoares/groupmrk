"""CLI for groupmrk - AI-powered bookmarks manager.

GroupMRK: Organize your browser bookmarks with AI.
GroupMRK: Organize seus favoritos do navegador com IA.

Commands / Comandos:
  import    - Import and organize bookmarks using AI
  search    - Search bookmarks using natural language
  export    - Export organized bookmarks to HTML
  organize  - Organize bookmarks into themes (AI or manual)

Usage / Uso:
  groupmrk import bookmarks.html --output organized.html --mock
  groupmrk search "python tutorials" bookmarks.html
  groupmrk organize bookmarks.html --max-themes 5

Security: All user inputs are validated and sanitized before processing.
Seguranca: Todas as entradas do usuario sao validadas e sanitizadas.
"""

import logging
import sys
from pathlib import Path

import click

from . import __version__
from .parser import BookmarkParser
from .output import HTMLOutputGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("groupmrk")


@click.group()
@click.version_option(version=__version__)
def main():
    """AI-powered browser bookmarks manager."""
    pass


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output", "-o", type=click.Path(), help="Output file for organized bookmarks"
)
@click.option(
    "--max-themes", type=int, default=10, help="Maximum number of theme categories"
)
@click.option(
    "--provider",
    type=click.Choice(["huggingface", "ollama"]),
    default="huggingface",
    help="AI provider to use",
)
@click.option(
    "--mock",
    is_flag=True,
    help="Use mock AI client (no API calls, for testing)",
)
def import_cmd(input_file, output, max_themes, provider, mock):
    """Import and organize bookmarks using AI."""
    logger.info(f"Starting import command for file: {input_file}")
    click.echo(f"Importing bookmarks from: {input_file}")

    logger.info("Step 1/4: Parsing HTML file")
    parser = BookmarkParser()
    collection = parser.parse_file(input_file)
    logger.info(f"Step 1/4 complete: Parsed {collection.metadata.total_count} bookmarks")
    click.echo(f"Parsed {collection.metadata.total_count} bookmarks")

    logger.info(f"Step 2/4: Organizing with AI (provider={provider}, max_themes={max_themes}, mock={mock})")
    from .graph import Orchestrator

    orchestrator = Orchestrator(provider=provider, max_themes=max_themes, mock=mock)
    collection = orchestrator.organize(collection)
    logger.info(f"Step 2/4 complete: Organized into {len(collection.themes)} themes")
    click.echo(f"Organized into {len(collection.themes)} themes")

    if not output:
        output = Path(input_file).with_suffix(".organized.html")
        logger.info(f"No output specified, using: {output}")

    logger.info(f"Step 3/4: Generating HTML output")
    generator = HTMLOutputGenerator()
    generator.write(collection, output)
    logger.info(f"Step 3/4 complete: HTML generated")
    logger.info(f"Step 4/4: Writing to file")
    click.echo(f"Output written to: {output}")
    logger.info(f"Import complete! Output: {output}")


@main.command()
@click.argument("query")
@click.argument("bookmark_file", type=click.Path(exists=True))
def search(query, bookmark_file):
    """Search bookmarks using natural language."""
    logger.info(f"Starting search: query='{query}', file={bookmark_file}")
    from .search import BookmarkSearch

    logger.info("Step 1/3: Parsing bookmark file")
    parser = BookmarkParser()
    collection = parser.parse_file(bookmark_file)
    logger.info(f"Step 1/3 complete: {len(collection.bookmarks)} bookmarks loaded")

    logger.info("Step 2/3: Searching with natural language")
    searcher = BookmarkSearch(collection)
    results = searcher.search(query)
    logger.info(f"Step 2/3 complete: Found {len(results)} results")

    if not results:
        click.echo("No results found.")
        logger.info("Search complete: No results")
        return

    click.echo(f"Found {len(results)} results:\n")
    for result in results:
        click.echo(f"  {result['bookmark'].title}")
        click.echo(f"    URL: {result['bookmark'].url}")
        click.echo(f"    Category: {result['bookmark'].effective_category}")
        click.echo(f"    Score: {result['score']:.2f}")
        if result.get("explanation"):
            click.echo(f"    Why: {result['explanation']}")
        click.echo()
    logger.info(f"Search complete: {len(results)} results shown")


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option(
    "--category",
    "-c",
    help="Filter by category/folder name",
)
def export(input_file, output_file, category):
    """Export organized bookmarks to HTML."""
    logger.info(f"Starting export: input={input_file}, output={output_file}, category={category}")
    parser = BookmarkParser()
    collection = parser.parse_file(input_file)

    if category:
        logger.info(f"Filtering by category: {category}")
        for bookmark in collection.bookmarks:
            if bookmark.theme != category and bookmark.manual_category != category:
                collection.bookmarks.remove(bookmark)

    logger.info("Generating HTML output")
    generator = HTMLOutputGenerator()
    generator.write(collection, output_file)

    click.echo(f"Exported {len(collection.bookmarks)} bookmarks to: {output_file}")
    logger.info(f"Export complete: {len(collection.bookmarks)} bookmarks exported")


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--set-category",
    "-s",
    nargs=2,
    type=str,
    help="Set category for bookmark (title pattern and new category)",
)
@click.option(
    "--max-themes", type=int, default=10, help="Maximum number of theme categories"
)
def organize(input_file, set_category, max_themes):
    """Organize bookmarks into themes."""
    logger.info(f"Starting organize: file={input_file}, set_category={set_category}, max_themes={max_themes}")
    parser = BookmarkParser()
    collection = parser.parse_file(input_file)

    if set_category:
        title_pattern, new_category = set_category
        logger.info(f"Manual category override: pattern='{title_pattern}', category='{new_category}'")
        count = 0
        for bookmark in collection.bookmarks:
            if title_pattern.lower() in bookmark.title.lower():
                bookmark.manual_category = new_category
                count += 1
        click.echo(f"Updated {count} bookmarks to category: {new_category}")
        logger.info(f"Category override complete: {count} bookmarks updated")
    else:
        logger.info("AI organization requested")
        from .graph import Orchestrator

        orchestrator = Orchestrator(max_themes=max_themes)
        collection = orchestrator.organize(collection)
        click.echo(f"Organized into {len(collection.themes)} themes")
        logger.info(f"AI organization complete: {len(collection.themes)} themes")

    logger.info("Generating output file")
    output_file = Path(input_file).with_suffix(".organized.html")
    generator = HTMLOutputGenerator()
    generator.write(collection, output_file)

    click.echo(f"Output written to: {output_file}")
    logger.info(f"Organize complete! Output: {output_file}")


if __name__ == "__main__":
    main()