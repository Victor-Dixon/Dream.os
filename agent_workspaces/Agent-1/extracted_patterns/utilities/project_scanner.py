import os
import ast
import json
import hashlib
import multiprocessing
from pathlib import Path
from typing import Dict, List, Union

# Try importing tree-sitter for Rust/JS/TS parsing
try:
    from tree_sitter import Language, Parser
except ImportError:
    Language = None
    Parser = None
    print("⚠️ tree-sitter not installed. Rust/JS/TS AST parsing will be partially disabled.")


CACHE_FILE = "dependency_cache.json"


class ProjectScanner:
    """
    A universal project scanner that:
      - Identifies Python, Rust, JavaScript, and TypeScript files.
      - Extracts functions, classes, and naive route definitions.
      - Caches file hashes to skip unchanged files.
      - Detects moved files by matching file hashes.
      - Writes a single JSON report (project_analysis.json) at the end.

    Extend or refactor `_save_report()` for modular outputs (e.g., routes.json, summary.md, etc.).
    """
    def __init__(self, project_root: Union[str, Path] = "."):
        """
        :param project_root: The root directory of the project to scan.
        """
        self.project_root = Path(project_root).resolve()
        self.analysis: Dict[str, Dict] = {}
        self.cache = self.load_cache()

        # Initialize tree-sitter parsers for Rust and JS
        # (You can add more languages as needed)
        self.rust_parser = self._init_tree_sitter_language("rust")
        self.js_parser = self._init_tree_sitter_language("javascript")

    def _init_tree_sitter_language(self, lang_name: str):
        """
        Initializes and returns a Parser for the given language name (e.g. "rust", "javascript")
        if we have a compiled tree-sitter grammar.

        Adjust the grammar_paths to point to your actual .so/.dll/.dylib files.
        """
        if not Language or not Parser:
            print(f"⚠️ tree-sitter not available. Skipping {lang_name} parser.")
            return None

        # Example paths to compiled grammars - you must update these to match your environment
        grammar_paths = {
            "rust": "path/to/tree-sitter-rust.so",
            "javascript": "path/to/tree-sitter-javascript.so",
        }

        if lang_name not in grammar_paths:
            print(f"⚠️ No grammar path for {lang_name}. Skipping.")
            return None

        grammar_path = grammar_paths[lang_name]
        if not Path(grammar_path).exists():
            print(f"⚠️ {lang_name} grammar not found at {grammar_path}")
            return None

        try:
            lang_lib = Language(grammar_path, lang_name)
            parser = Parser()
            parser.set_language(lang_lib)
            return parser
        except Exception as e:
            print(f"⚠️ Failed to initialize tree-sitter {lang_name} parser: {e}")
            return None

    def load_cache(self) -> Dict:
        """
        Loads a JSON cache from disk if present.
        The cache stores file paths, hashes, etc. to skip re-analysis of unchanged files.
        """
        if Path(CACHE_FILE).exists():
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_cache(self):
        """
        Writes the updated cache to disk so subsequent runs can detect unchanged or moved files quickly.
        """
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=4)

    def hash_file(self, file_path: Path) -> str:
        """
        Calculates an MD5 hash of a file's content.

        :param file_path: Path to the file to hash.
        :return: Hex digest string, or "" if an error occurs.
        """
        try:
            with file_path.open("rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def scan_project(self):
        """
        Orchestrates the project scan:
          - Finds Python, Rust, JS, TS files.
          - Excludes certain directories.
          - Detects moved files by comparing cached hashes.
          - Multiprocesses each file for analysis.
          - Saves a single JSON report 'project_analysis.json'.
        """
        print(f"🔍 Scanning project: {self.project_root} ...")

        # Gather all relevant files
        python_files = list(self.project_root.rglob("*.py"))
        rust_files = list(self.project_root.rglob("*.rs"))
        js_files = list(self.project_root.rglob("*.js"))
        ts_files = list(self.project_root.rglob("*.ts"))

        all_files = python_files + rust_files + js_files + ts_files
        valid_files = [f for f in all_files if not self._should_exclude(f)]

        # Track old vs. new paths
        previous_files = set(self.cache.keys())
        current_files = {str(f.relative_to(self.project_root)) for f in valid_files}

        moved_files = {}
        missing_files = previous_files - current_files

        # Detect moved files by matching file hashes
        for old_path in previous_files:
            old_hash = self.cache.get(old_path, {}).get("hash")
            if not old_hash:
                continue
            for new_path in current_files:
                new_file = self.project_root / new_path
                if self.hash_file(new_file) == old_hash:
                    moved_files[old_path] = new_path
                    break

        # Remove truly missing files from cache
        for missing_file in missing_files:
            if missing_file not in moved_files:
                del self.cache[missing_file]

        # Update cache for moved files
        for old_path, new_path in moved_files.items():
            self.cache[new_path] = self.cache.pop(old_path)

        # Multiprocessing to speed up analysis
        with multiprocessing.Pool(processes=os.cpu_count()) as pool:
            results = pool.map(self._process_file, valid_files)

        # Collect results
        for file_result in results:
            if file_result:
                file_path, analysis_result = file_result
                self.analysis[file_path] = analysis_result

        # Write final report and cache
        self._save_report()
        self.save_cache()
        print(f"✅ Scan complete. Results saved to {self.project_root / 'project_analysis.json'}")

    def _should_exclude(self, file_path: Path) -> bool:
        """
        Excludes certain directories from scanning, like virtualenvs or build artifacts.
        Adjust as needed for your environment.
        """
        exclude_dirs = {
            "venv",
            "__pycache__",
            "node_modules",
            "migrations",
            "build",
            "target",
            ".git",
            "coverage",
        }
        return any(excluded in file_path.parts for excluded in exclude_dirs)

    def _process_file(self, file_path: Path):
        """
        Handles analysis of a single file:
          - Skips if the file is unchanged (hash match).
          - Reads its source, dispatches to the appropriate parser.
          - Updates the cache with the new hash.
        """
        file_hash = self.hash_file(file_path)
        relative_path = str(file_path.relative_to(self.project_root))

        # If unchanged, skip
        if relative_path in self.cache and self.cache[relative_path]["hash"] == file_hash:
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            analysis_result = self._analyze_file_by_language(file_path, source_code)

            # Update cache
            self.cache[relative_path] = {"hash": file_hash}
            return (relative_path, analysis_result)

        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return None

    def _analyze_file_by_language(self, file_path: Path, source_code: str) -> Dict:
        """
        Dispatches analysis based on file extension and available parsers.
        Returns a dictionary with keys like:
          {
            "language": "python"|"rust"|"javascript"|...,
            "functions": [...],
            "classes": {...},
            "routes": [...],
          }
        """
        suffix = file_path.suffix.lower()
        if suffix == ".py":
            data = self._analyze_python(source_code)
            return {
                "language": "python",
                "functions": data["functions"],
                "classes": data["classes"],
                "routes": data.get("routes", []),
            }
        elif suffix == ".rs" and self.rust_parser:
            data = self._analyze_rust(source_code)
            return {
                "language": "rust",
                "functions": data["functions"],
                "classes": data["classes"],
            }
        elif suffix in [".js", ".ts"] and self.js_parser:
            data = self._analyze_javascript(source_code)
            return {
                "language": "javascript",
                "functions": data["functions"],
                "classes": data["classes"],
                "routes": data["routes"],
            }
        else:
            # If no parser or unrecognized file type
            return {"language": suffix, "functions": [], "classes": {}, "routes": []}

    def _analyze_python(self, source_code: str) -> Dict:
        """
        Extracts:
          - function names
          - class names -> method names
          - naive route detection if using Flask-like decorators, e.g.,
            @app.route("/path", methods=["GET","POST"])

        Expand this to match your framework (Django, FastAPI, etc.) if needed.
        """
        tree = ast.parse(source_code)
        functions = []
        classes = {}
        routes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

                # Check for route-like decorators
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and hasattr(decorator.func, 'attr'):
                        func_attr = decorator.func.attr.lower()
                        # e.g., route, get, post, etc.
                        if func_attr in {"route", "get", "post", "put", "delete", "patch"}:
                            path_arg = "/unknown"
                            methods = [func_attr.upper()]  # default if not provided

                            # If there's a string arg, we treat it as the route path
                            if decorator.args:
                                arg0 = decorator.args[0]
                                if isinstance(arg0, ast.Str):
                                    path_arg = arg0.s

                            # If there's a 'methods=["GET","POST"]' keyword
                            for kw in decorator.keywords:
                                if kw.arg == "methods" and isinstance(kw.value, ast.List):
                                    # e.g. methods=["GET","POST"]
                                    extracted_methods = []
                                    for elt in kw.value.elts:
                                        if isinstance(elt, ast.Str):
                                            extracted_methods.append(elt.s.upper())
                                    if extracted_methods:
                                        methods = extracted_methods

                            # Create a route entry for each method
                            for m in methods:
                                routes.append({
                                    "function": node.name,
                                    "method": m,
                                    "path": path_arg
                                })

            elif isinstance(node, ast.ClassDef):
                method_names = [
                    m.name for m in node.body if isinstance(m, ast.FunctionDef)
                ]
                classes[node.name] = method_names

        return {"functions": functions, "classes": classes, "routes": routes}

    def _analyze_rust(self, source_code: str) -> Dict:
        """
        Uses tree-sitter to extract:
          - functions
          - structs -> methods (impl blocks)
        (No route detection by default in Rust, but you could expand if you
         use frameworks like Rocket or Actix.)
        """
        if not self.rust_parser:
            return {"functions": [], "classes": {}}

        tree = self.rust_parser.parse(bytes(source_code, "utf-8"))
        functions = []
        classes = {}

        def _traverse(node):
            if node.type == "function_item":
                fn_name_node = node.child_by_field_name("name")
                if fn_name_node:
                    fn_name = fn_name_node.text.decode("utf-8")
                    functions.append(fn_name)
            elif node.type == "struct_item":
                struct_name_node = node.child_by_field_name("name")
                if struct_name_node:
                    struct_name = struct_name_node.text.decode("utf-8")
                    classes[struct_name] = []
            elif node.type == "impl_item":
                impl_type_node = node.child_by_field_name("type")
                if impl_type_node:
                    impl_name = impl_type_node.text.decode("utf-8")
                    if impl_name not in classes:
                        classes[impl_name] = []
                    # Look for function_item children
                    for child in node.children:
                        if child.type == "function_item":
                            method_node = child.child_by_field_name("name")
                            if method_node:
                                method_name = method_node.text.decode("utf-8")
                                classes[impl_name].append(method_name)

            for child in node.children:
                _traverse(child)

        _traverse(tree.root_node)
        return {"functions": functions, "classes": classes}

    def _analyze_javascript(self, source_code: str) -> Dict:
        """
        Extracts:
          - function declarations
          - class declarations
          - arrow functions assigned to a variable
          - basic Express route calls (app.get("/path", ...) or router.post("/path", ...))

        This is naive. For more robust detection (e.g. router.route('/').get(...).post(...)),
        you'd need deeper parsing or expansions.
        """
        if not self.js_parser:
            return {"functions": [], "classes": {}, "routes": []}

        tree = self.js_parser.parse(bytes(source_code, "utf-8"))
        root = tree.root_node

        functions = []
        classes = {}
        routes = []

        def get_node_text(node):
            return node.text.decode("utf-8")

        def _traverse(node):
            node_type = node.type

            # Named function declarations: function foo() { ... }
            if node_type == "function_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    fn_name = get_node_text(name_node)
                    functions.append(fn_name)

            # Class declarations: class Foo { ... }
            elif node_type == "class_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    cls_name = get_node_text(name_node)
                    classes[cls_name] = []

            # Arrow functions in lexical_declaration: const foo = () => {}
            elif node_type == "lexical_declaration":
                for child in node.children:
                    if child.type == "variable_declarator":
                        name_node = child.child_by_field_name("name")
                        value_node = child.child_by_field_name("value")
                        if name_node and value_node and value_node.type == "arrow_function":
                            fn_name = get_node_text(name_node)
                            functions.append(fn_name)

            # Basic detection for app.get("/path", ...) or router.post("/path", ...)
            elif node_type == "call_expression":
                if node.child_count >= 2:
                    callee_node = node.child_by_field_name("function")
                    args_node = node.child_by_field_name("arguments")

                    if callee_node:
                        callee_text = get_node_text(callee_node)
                        parts = callee_text.split(".")
                        if len(parts) == 2:
                            obj, method = parts
                            method_lower = method.lower()
                            if method_lower in {"get", "post", "put", "delete", "patch"}:
                                path_str = "/unknown"
                                if args_node and args_node.child_count > 0:
                                    first_arg = args_node.child(0)
                                    # Check if the first argument is a string
                                    if first_arg.type == "string":
                                        path_text = get_node_text(first_arg)
                                        path_str = path_text.strip('"\'')
                                routes.append({
                                    "object": obj,
                                    "method": method_upper(method_lower),
                                    "path": path_str
                                })

            # Recurse into children
            for child in node.children:
                _traverse(child)

        def method_upper(m: str) -> str:
            return m.upper() if m else ""

        _traverse(root)
        return {"functions": functions, "classes": classes, "routes": routes}

    def _save_report(self):
        """
        Writes the final self.analysis dictionary to a single JSON file.
        Modify this method to produce multiple files or advanced HTML/Markdown outputs.
        """
        report_path = self.project_root / "project_analysis.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.analysis, f, indent=4)


if __name__ == "__main__":
    # Example usage: python project_scanner.py
    scanner = ProjectScanner(project_root=".")
    scanner.scan_project()
