"""
Unit tests for src/services/work_indexer.py

Tests work indexer functionality including:
- Initialization with/without vector DB
- Agent work indexing
- Inbox message indexing
- File handling and error cases
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

from src.services.work_indexer import WorkIndexer


class TestWorkIndexer:
    """Test work indexer."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_dir = Path(tmpdir) / "agent_workspaces" / "Agent-3"
            workspace_dir.mkdir(parents=True)
            inbox_dir = workspace_dir / "inbox"
            inbox_dir.mkdir()
            
            # Create sample files
            test_file = workspace_dir / "test_file.py"
            test_file.write_text("print('test')")
            
            message_file = inbox_dir / "message1.md"
            message_file.write_text("# Test message\n\nContent here")
            
            yield tmpdir

    @pytest.fixture
    def indexer_with_vector_db(self, temp_workspace):
        """Create indexer with vector DB available."""
        with patch('src.services.work_indexer.get_vector_database_service') as mock_get, \
             patch('src.services.work_indexer.add_document_to_vector_db') as mock_add:
            mock_vector_db = MagicMock()
            mock_get.return_value = mock_vector_db
            
            # Mock successful add result
            mock_result = MagicMock()
            mock_result.success = True
            mock_result.message = "Success"
            mock_add.return_value = mock_result
            
            # Patch workspace path
            with patch('src.services.work_indexer.Path') as mock_path_class:
                workspace_path = Path(temp_workspace) / "agent_workspaces" / "Agent-3"
                mock_path_class.return_value = workspace_path
                
                indexer = WorkIndexer("Agent-3")
                indexer.workspace_path = workspace_path
                return indexer

    @pytest.fixture
    def indexer_without_vector_db(self, temp_workspace):
        """Create indexer without vector DB."""
        with patch('src.services.work_indexer.get_vector_database_service') as mock_get:
            mock_get.side_effect = ImportError("Vector DB not available")
            
            # Patch workspace path
            with patch('src.services.work_indexer.Path') as mock_path_class:
                workspace_path = Path(temp_workspace) / "agent_workspaces" / "Agent-3"
                mock_path_class.return_value = workspace_path
                
                indexer = WorkIndexer("Agent-3")
                indexer.workspace_path = workspace_path
                return indexer

    def test_init_with_vector_db(self, indexer_with_vector_db):
        """Test initialization with vector database."""
        assert indexer_with_vector_db.agent_id == "Agent-3"
        assert indexer_with_vector_db.vector_integration["status"] == "connected"

    def test_init_without_vector_db(self, indexer_without_vector_db):
        """Test initialization without vector database."""
        assert indexer_without_vector_db.agent_id == "Agent-3"
        assert indexer_without_vector_db.vector_integration["status"] == "disconnected"

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_success(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test successful agent work indexing."""
        # Mock successful result
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.message = "Success"
        mock_add.return_value = mock_result
        
        # Create test file
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test_code.py"
        test_file.write_text("def test_function():\n    pass")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        mock_add.assert_called_once()

    def test_index_agent_work_file_not_found(self, indexer_with_vector_db):
        """Test indexing when file doesn't exist."""
        result = indexer_with_vector_db.index_agent_work("nonexistent_file.py", "code")
        
        assert result is False

    def test_index_agent_work_empty_file(self, indexer_with_vector_db, temp_workspace):
        """Test indexing empty file."""
        # Create empty file
        empty_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "empty.py"
        empty_file.write_text("")
        
        result = indexer_with_vector_db.index_agent_work(str(empty_file), "code")
        
        assert result is False

    def test_index_agent_work_no_vector_db(self, indexer_without_vector_db, temp_workspace):
        """Test indexing when vector DB not available."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_without_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    def test_index_agent_work_add_failure(self, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing when add_document fails."""
        # Mock failed result
        mock_result = MagicMock()
        mock_result.success = False
        mock_result.message = "Failed"
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    def test_index_agent_work_exception(self, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing exception handling."""
        mock_add.side_effect = Exception("Test error")
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_success(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test successful inbox message indexing."""
        # Mock successful result
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.message = "Success"
        mock_add.return_value = mock_result
        
        # Mock VectorDocument to accept any kwargs
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        # Clear existing messages and create new ones
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        # Remove existing files
        for existing_file in inbox_dir.glob("*.md"):
            existing_file.unlink()
        
        # Create message files
        msg1 = inbox_dir / "msg1.md"
        msg1.write_text("# Message 1\n\nContent")
        msg2 = inbox_dir / "msg2.md"
        msg2.write_text("# Message 2\n\nMore content")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 2
        assert mock_add.call_count == 2

    def test_index_inbox_messages_no_inbox(self, indexer_with_vector_db, temp_workspace):
        """Test indexing when inbox directory doesn't exist."""
        # Remove inbox directory
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        if inbox_dir.exists():
            shutil.rmtree(inbox_dir)
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 0

    def test_index_inbox_messages_no_vector_db(self, indexer_without_vector_db, temp_workspace):
        """Test indexing when vector DB not available."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg1 = inbox_dir / "msg1.md"
        msg1.write_text("# Message")
        
        count = indexer_without_vector_db.index_inbox_messages()
        
        assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    def test_index_inbox_messages_empty_file(self, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing skips empty message files."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        empty_msg = inbox_dir / "empty.md"
        empty_msg.write_text("")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_add_failure(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing when add_document fails for some messages."""
        # Mock VectorDocument to accept any kwargs
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        # Mock mixed results
        mock_result_success = MagicMock()
        mock_result_success.success = True
        mock_result_failure = MagicMock()
        mock_result_failure.success = False
        mock_result_failure.message = "Failed"
        mock_add.side_effect = [mock_result_success, mock_result_failure]
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg1 = inbox_dir / "msg1.md"
        msg1.write_text("# Message 1")
        msg2 = inbox_dir / "msg2.md"
        msg2.write_text("# Message 2")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        # Should only count successful ones
        assert count == 1

    @patch('src.services.work_indexer.add_document_to_vector_db')
    def test_index_inbox_messages_exception_handling(self, mock_add, indexer_with_vector_db, temp_workspace):
        """Test exception handling during message indexing."""
        mock_add.side_effect = Exception("Test error")
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg1 = inbox_dir / "msg1.md"
        msg1.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        # Should handle exception gracefully
        assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    def test_index_inbox_messages_read_error(self, mock_add, indexer_with_vector_db, temp_workspace):
        """Test handling read errors for message files."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg1 = inbox_dir / "msg1.md"
        msg1.write_text("# Message")
        
        # Mock read error
        with patch('pathlib.Path.read_text', side_effect=IOError("Read error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    def test_init_with_config_path(self, temp_workspace):
        """Test initialization with config_path parameter."""
        with patch('src.services.work_indexer.get_vector_database_service') as mock_get:
            mock_get.return_value = MagicMock()
            
            indexer = WorkIndexer("Agent-3", config_path="custom/path")
            
            assert indexer.agent_id == "Agent-3"
            # config_path is accepted but not currently used
            assert indexer.workspace_path is not None

    def test_init_vector_db_exception(self, temp_workspace):
        """Test initialization when vector DB raises exception."""
        with patch('src.services.work_indexer.get_vector_database_service') as mock_get:
            mock_get.side_effect = Exception("Connection error")
            
            indexer = WorkIndexer("Agent-3")
            
            assert indexer.vector_integration["status"] == "disconnected"
            assert "error" in indexer.vector_integration

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_different_work_types(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing with different work types."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        work_types = ["code", "documentation", "test", "config"]
        for work_type in work_types:
            result = indexer_with_vector_db.index_agent_work(str(test_file), work_type)
            assert result is True

    @patch('src.services.work_indexer.add_document_to_vector_db')
    def test_index_agent_work_read_error(self, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing when file read fails."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('pathlib.Path.read_text', side_effect=IOError("Read error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    def test_index_agent_work_document_creation_error(self, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing when document creation fails."""
        mock_doc_class.side_effect = Exception("Document creation error")
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_whitespace_only(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing skips whitespace-only message files."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        whitespace_msg = inbox_dir / "whitespace.md"
        whitespace_msg.write_text("   \n\t  \n")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_multiple_files(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing multiple message files."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        for i in range(5):
            msg_file = inbox_dir / f"msg{i}.md"
            msg_file.write_text(f"# Message {i}\n\nContent {i}")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 5
        assert mock_add.call_count == 5

    def test_index_inbox_messages_path_error(self, indexer_with_vector_db):
        """Test indexing when workspace path access fails."""
        with patch('pathlib.Path.__truediv__', side_effect=Exception("Path error")):
            count = indexer_with_vector_db.index_inbox_messages()
            assert count == 0

    def test_workspace_path_construction(self):
        """Test workspace path construction."""
        with patch('src.services.work_indexer.get_vector_database_service') as mock_get:
            mock_get.return_value = MagicMock()
            
            indexer = WorkIndexer("Agent-7")
            
            assert "agent_workspaces" in str(indexer.workspace_path)
            assert "Agent-7" in str(indexer.workspace_path)

    def test_logger_initialization(self):
        """Test logger is properly initialized."""
        with patch('src.services.work_indexer.get_vector_database_service') as mock_get:
            mock_get.return_value = MagicMock()
            
            indexer = WorkIndexer("Agent-3")
            
            assert indexer.logger is not None
            assert hasattr(indexer.logger, 'info')
            assert hasattr(indexer.logger, 'warning')
            assert hasattr(indexer.logger, 'error')

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_with_embedding(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing with embedding data."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("def test(): pass")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_metadata_structure(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that indexed document has correct metadata structure."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with proper metadata
        assert mock_doc_class.called

    def test_index_agent_work_path_object(self, indexer_with_vector_db, temp_workspace):
        """Test indexing accepts Path object."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('src.services.work_indexer.add_document_to_vector_db') as mock_add:
            mock_result = MagicMock()
            mock_result.success = True
            mock_add.return_value = mock_result
            
            result = indexer_with_vector_db.index_agent_work(test_file, "code")
            
            assert result is True

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_no_md_files(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing when no .md files exist."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        # Create non-md file
        txt_file = inbox_dir / "message.txt"
        txt_file.write_text("Not a markdown file")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_with_message_id(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing message with specific ID format."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "CAPTAIN_MESSAGE_20250101_123456.md"
        msg_file.write_text("# Captain Message\n\nContent")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1

    def test_index_agent_work_unicode_content(self, indexer_with_vector_db, temp_workspace):
        """Test indexing file with unicode content."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "unicode.py"
        test_file.write_text("# Test with émojis 🚀 and unicode: 测试")
        
        with patch('src.services.work_indexer.add_document_to_vector_db') as mock_add:
            mock_result = MagicMock()
            mock_result.success = True
            mock_add.return_value = mock_result
            
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is True

    def test_index_agent_work_very_large_file(self, indexer_with_vector_db, temp_workspace):
        """Test indexing very large file."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "large.py"
        # Create large content
        large_content = "# Large file\n" + "x" * 100000
        test_file.write_text(large_content)
        
        with patch('src.services.work_indexer.add_document_to_vector_db') as mock_add:
            mock_result = MagicMock()
            mock_result.success = True
            mock_add.return_value = mock_result
            
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is True

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_document_id_format(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that document ID includes agent_id and filename."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_metadata_includes_file_size(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that metadata includes file_size."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        content = "test content" * 100
        test_file.write_text(content)
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with metadata
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_skips_non_md_files(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that only .md files are indexed."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        # Create non-md file
        txt_file = inbox_dir / "message.txt"
        txt_file.write_text("Not markdown")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        # Should not index .txt files
        assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_handles_encoding_errors(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test handling of encoding errors when reading messages."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        # Mock encoding error
        with patch('pathlib.Path.read_text', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    def test_index_agent_work_handles_permission_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of permission errors when reading file."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('pathlib.Path.read_text', side_effect=PermissionError("Permission denied")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_tags_format(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that tags are formatted correctly."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with tags
        assert mock_doc_class.called

    def test_index_inbox_messages_handles_glob_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of glob errors."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        
        with patch('pathlib.Path.glob', side_effect=Exception("Glob error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_timestamp_in_id(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that document ID includes timestamp."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with ID containing timestamp
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_indexed_at_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that metadata includes indexed_at timestamp."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with indexed_at in metadata
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_indexed_at_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that inbox message metadata includes indexed_at."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with indexed_at in metadata
        assert mock_doc_class.called

    def test_index_agent_work_handles_file_stat_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of file stat errors."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('pathlib.Path.stat', side_effect=OSError("Stat error")):
            with patch('src.services.work_indexer.add_document_to_vector_db') as mock_add:
                mock_result = MagicMock()
                mock_result.success = True
                mock_add.return_value = mock_result
                
                result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
                
                # Should handle stat error gracefully
                assert result is True or result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_source_file_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that source_file is included in document."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with source_file
        assert mock_doc_class.called

    def test_index_inbox_messages_handles_directory_access_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of directory access errors."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        
        with patch('pathlib.Path.exists', side_effect=OSError("Access error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            # Should handle access error gracefully
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_message_file_name_in_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that message_file name is in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "CAPTAIN_MESSAGE_123.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with message_file in metadata
        assert mock_doc_class.called

    def test_index_agent_work_handles_path_resolution_error(self, indexer_with_vector_db):
        """Test handling of path resolution errors."""
        with patch('pathlib.Path', side_effect=Exception("Path error")):
            result = indexer_with_vector_db.index_agent_work("test.py", "code")
            
            assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_document_type_enum(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that DocumentType enum is used correctly."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify DocumentType was called
        assert mock_doc_type.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_collection_name(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that collection name is passed correctly."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify add_document_to_vector_db was called with "agent_work" collection
        assert mock_add.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_collection_name(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that inbox messages use correct collection name."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify add_document_to_vector_db was called with "agent_messages" collection
        assert mock_add.called

    def test_index_agent_work_handles_file_not_readable(self, indexer_with_vector_db, temp_workspace):
        """Test handling when file exists but is not readable."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('pathlib.Path.read_text', side_effect=PermissionError("Not readable")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_agent_id_in_tags(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that agent_id is included in tags."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with agent_id in tags
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_work_type_in_tags(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that work_type is included in tags."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "documentation")
        
        assert result is True
        # Verify VectorDocument was called with work_type in tags
        assert mock_doc_class.called

    def test_index_inbox_messages_handles_file_not_readable(self, indexer_with_vector_db, temp_workspace):
        """Test handling when inbox message file is not readable."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('pathlib.Path.read_text', side_effect=PermissionError("Not readable")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_inbox_message_tag(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that inbox messages have 'type:inbox_message' tag."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with inbox_message tag
        assert mock_doc_class.called

    def test_index_agent_work_handles_os_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of general OS errors."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('pathlib.Path.exists', side_effect=OSError("OS error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_file_size_in_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that file_size is included in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        content = "test content" * 100
        test_file.write_text(content)
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with file_size in metadata
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_work_type_in_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that work_type is included in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "test_type")
        
        assert result is True
        # Verify VectorDocument was called with work_type in metadata
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_agent_id_in_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that agent_id is included in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with agent_id in metadata
        assert mock_doc_class.called

    def test_index_agent_work_handles_file_not_found_during_read(self, indexer_with_vector_db, temp_workspace):
        """Test handling when file disappears between exists() and read_text()."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('pathlib.Path.read_text', side_effect=FileNotFoundError("File not found")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_agent_id_in_tags(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that agent_id is included in inbox message tags."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with agent_id in tags
        assert mock_doc_class.called

    def test_index_inbox_messages_handles_file_not_found_during_read(self, indexer_with_vector_db, temp_workspace):
        """Test handling when inbox file disappears between glob() and read_text()."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('pathlib.Path.read_text', side_effect=FileNotFoundError("File not found")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_message_file_name_format(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that message file name format is preserved in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "CAPTAIN_MESSAGE_20250101_123456_abc123.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with message_file in metadata
        assert mock_doc_class.called

    def test_index_agent_work_handles_value_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of ValueError during indexing."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('src.services.work_indexer.VectorDocument', side_effect=ValueError("Value error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    def test_index_inbox_messages_handles_value_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of ValueError during inbox indexing."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('src.services.work_indexer.VectorDocument', side_effect=ValueError("Value error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    def test_index_agent_work_handles_type_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of TypeError during indexing."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('src.services.work_indexer.datetime', side_effect=TypeError("Type error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    def test_index_inbox_messages_handles_type_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of TypeError during inbox indexing."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('src.services.work_indexer.datetime', side_effect=TypeError("Type error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_indexed_at_timestamp(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that indexed_at timestamp is included in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with indexed_at in metadata
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_document_id_format(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that document ID format includes timestamp."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with properly formatted document ID
        assert mock_doc_class.called

    def test_index_agent_work_handles_key_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of KeyError during indexing."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('src.services.work_indexer.Path.stat', side_effect=KeyError("Key error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    def test_index_inbox_messages_handles_key_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of KeyError during inbox indexing."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('src.services.work_indexer.Path.stat', side_effect=KeyError("Key error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_indexed_at_timestamp(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that indexed_at timestamp is included in inbox message metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with indexed_at in metadata
        assert mock_doc_class.called

    def test_index_agent_work_handles_attribute_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of AttributeError during indexing."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('src.services.work_indexer.Path.exists', side_effect=AttributeError("Attribute error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    def test_index_inbox_messages_handles_attribute_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of AttributeError during inbox indexing."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('pathlib.Path.glob', side_effect=AttributeError("Attribute error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_source_file_absolute_path(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that source_file uses absolute path in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with absolute path in source_file
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_message_file_absolute_path(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that message_file uses absolute path in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with absolute path in message_file
        assert mock_doc_class.called

    def test_index_agent_work_handles_io_error_during_stat(self, indexer_with_vector_db, temp_workspace):
        """Test handling of IOError during file stat."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('pathlib.Path.stat', side_effect=IOError("IO error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    def test_index_inbox_messages_handles_io_error_during_stat(self, indexer_with_vector_db, temp_workspace):
        """Test handling of IOError during inbox file stat."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('pathlib.Path.stat', side_effect=IOError("IO error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_content_preview_in_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that content preview is included in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        content = "test content" * 100
        test_file.write_text(content)
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with content preview in metadata
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_file_extension_in_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that file extension is included in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with file extension in metadata
        assert mock_doc_class.called

    def test_index_agent_work_handles_runtime_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of RuntimeError during indexing."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('src.services.work_indexer.VectorDocument', side_effect=RuntimeError("Runtime error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    def test_index_inbox_messages_handles_runtime_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of RuntimeError during inbox indexing."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('src.services.work_indexer.VectorDocument', side_effect=RuntimeError("Runtime error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_file_name_in_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that file name is included in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with file name in metadata
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_message_timestamp_in_metadata(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that message timestamp is included in metadata."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "CAPTAIN_MESSAGE_20250101_123456_abc123.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with message timestamp in metadata
        assert mock_doc_class.called

    def test_index_agent_work_handles_memory_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of MemoryError during indexing."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        with patch('pathlib.Path.read_text', side_effect=MemoryError("Memory error")):
            result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
            
            assert result is False

    def test_index_inbox_messages_handles_memory_error(self, indexer_with_vector_db, temp_workspace):
        """Test handling of MemoryError during inbox indexing."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        msg_file.write_text("# Message")
        
        with patch('pathlib.Path.read_text', side_effect=MemoryError("Memory error")):
            count = indexer_with_vector_db.index_inbox_messages()
            
            assert count == 0

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_relative_path_handling(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that relative paths are converted to absolute paths."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        # Use relative path
        relative_path = "agent_workspaces/Agent-3/test.py"
        result = indexer_with_vector_db.index_agent_work(relative_path, "code")
        
        assert result is True
        # Verify VectorDocument was called with absolute path
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_multiple_agents(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test indexing inbox messages for multiple agents."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        # Create inbox for multiple agents
        for agent_id in ["Agent-1", "Agent-2", "Agent-3"]:
            inbox_dir = Path(temp_workspace) / "agent_workspaces" / agent_id / "inbox"
            msg_file = inbox_dir / "message.md"
            msg_file.write_text("# Message")
        
        # Index for Agent-3 (the fixture agent)
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1  # Only Agent-3's inbox
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_document_id_uniqueness(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that document IDs are unique."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        # Index same file twice
        result1 = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        result2 = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result1 is True
        assert result2 is True
        # Verify VectorDocument was called with unique IDs
        assert mock_doc_class.call_count == 2

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_metadata_completeness(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that all required metadata fields are included."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with complete metadata
        assert mock_doc_class.called

    def test_index_agent_work_handles_unicode_file_name(self, indexer_with_vector_db, temp_workspace):
        """Test handling of unicode characters in file name."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test_测试.py"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        # Should handle unicode file names
        assert result is True

    def test_index_inbox_messages_handles_unicode_file_name(self, indexer_with_vector_db, temp_workspace):
        """Test handling of unicode characters in inbox file name."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message_测试.md"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        # Should handle unicode file names
        assert count == 1

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_content_encoding_utf8(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that content is read with UTF-8 encoding."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "test.py"
        content = "test content with émojis 🚀 and unicode: 测试"
        test_file.write_text(content, encoding='utf-8')
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Verify VectorDocument was called with UTF-8 content
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_content_encoding_utf8(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test that inbox message content is read with UTF-8 encoding."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message.md"
        content = "# Message with émojis 🚀 and unicode: 测试"
        msg_file.write_text(content, encoding='utf-8')
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Verify VectorDocument was called with UTF-8 content
        assert mock_doc_class.called

    def test_index_agent_work_handles_file_with_no_extension(self, indexer_with_vector_db, temp_workspace):
        """Test handling of file with no extension."""
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "testfile"
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        # Should handle files without extensions
        assert result is True

    def test_index_inbox_messages_handles_file_with_no_extension(self, indexer_with_vector_db, temp_workspace):
        """Test handling of inbox file with no extension."""
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        msg_file = inbox_dir / "message"
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        # Should handle files without extensions
        assert count == 1

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_agent_work_very_long_file_name(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test handling of very long file names."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        long_name = "a" * 200 + ".py"
        test_file = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / long_name
        test_file.write_text("test content")
        
        result = indexer_with_vector_db.index_agent_work(str(test_file), "code")
        
        assert result is True
        # Should handle very long file names
        assert mock_doc_class.called

    @patch('src.services.work_indexer.add_document_to_vector_db')
    @patch('src.services.work_indexer.VectorDocument')
    @patch('src.services.work_indexer.DocumentType')
    def test_index_inbox_messages_very_long_file_name(self, mock_doc_type, mock_doc_class, mock_add, indexer_with_vector_db, temp_workspace):
        """Test handling of very long inbox file names."""
        mock_result = MagicMock()
        mock_result.success = True
        mock_add.return_value = mock_result
        
        mock_doc_instance = MagicMock()
        mock_doc_class.return_value = mock_doc_instance
        
        inbox_dir = Path(temp_workspace) / "agent_workspaces" / "Agent-3" / "inbox"
        long_name = "a" * 200 + ".md"
        msg_file = inbox_dir / long_name
        msg_file.write_text("# Message")
        
        count = indexer_with_vector_db.index_inbox_messages()
        
        assert count == 1
        # Should handle very long file names
        assert mock_doc_class.called

