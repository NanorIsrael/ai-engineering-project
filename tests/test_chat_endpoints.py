# import os 
# import sys
# from pathlib import Path
# import unittest

# # This allows importing app from the parent directory
# sys.path.insert(0, str(Path(__file__).parent.parent))

# import pytest
# import json
# from unittest.mock import patch, MagicMock

# class TestChatEndpoint:
#     """Test suite for /chat endpoint"""
    
#     def test_chat_successful_response(self, client, sample_messages):
#         """Test successful chat response"""
#         response = client.post(
#             '/chat',
#             json=sample_messages["valid_message"],
#             content_type='application/json'
#         )
        
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert "reply" in data
#         assert data["reply"] == "Hi human"
    
#     def test_chat_with_empty_message(self, client, sample_messages):
#         """Test chat with empty message returns 400 error"""
#         response = client.post(
#             '/chat',
#             json=sample_messages["empty_message"],
#             content_type='application/json'
#         )
        
#         assert response.status_code == 400
#         data = json.loads(response.data)
#         assert "error" in data
#         assert data["error"] == "Empty message"
    
#     def test_chat_with_whitespace_message(self, client, sample_messages):
#         """Test chat with whitespace-only message returns 400 error"""
#         response = client.post(
#             '/chat',
#             json=sample_messages["whitespace_message"],
#             content_type='application/json'
#         )
        
#         assert response.status_code == 400
#         data = json.loads(response.data)
#         assert data["error"] == "Empty message"
    
#     def test_chat_with_missing_message_field(self, client):
#         """Test chat with missing 'message' field"""
#         response = client.post(
#             '/chat',
#             json={},
#             content_type='application/json'
#         )
        
#         assert response.status_code == 400
#         data = json.loads(response.data)
#         assert "error" in data
    
#     def test_chat_with_no_json_body(self, client):
#         """Test chat with no JSON body"""
#         response = client.post(
#             '/chat',
#             data="not json",
#             content_type='text/plain'
#         )
        
#         # Should either be 400 or 415 depending on your error handling
#         assert response.status_code in [400, 415, 500]
    
#     def test_chat_preserves_conversation_history(self, client):
#         """Test that conversation history is preserved across requests"""
#         # First message
#         response1 = client.post(
#             '/chat',
#             json={"message": "First message"},
#             content_type='application/json'
#         )
#         assert response1.status_code == 200
        
#         # Second message
#         response2 = client.post(
#             '/chat',
#             json={"message": "Second message"},
#             content_type='application/json'
#         )
#         assert response2.status_code == 200
        
#         # Check session history
#         with client.session_transaction() as sess:
#             history = sess.get("history", [])
#             assert len(history) == 4  # 2 user + 2 assistant messages
#             assert history[0]["role"] == "user"
#             assert history[0]["content"] == "First message"
#             assert history[1]["role"] == "assistant"
#             assert history[2]["role"] == "user"
#             assert history[2]["content"] == "Second message"
    
#     def test_chat_handles_long_messages(self, client, sample_messages):
#         """Test chat with very long messages"""
#         response = client.post(
#             '/chat',
#             json=sample_messages["long_message"],
#             content_type='application/json'
#         )
        
#         # Should handle long messages (may want to add size limits)
#         assert response.status_code == 200
    
#     def test_chat_with_unicode_messages(self, client, sample_messages):
#         """Test chat with Unicode/emoji messages"""
#         response = client.post(
#             '/chat',
#             json=sample_messages["unicode_message"],
#             content_type='application/json'
#         )
        
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert "reply" in data

#     @unittest.skip("")
#     @patch('app.session')
#     def test_chat_session_history_initialization(self, mock_session, client):
#         """Test that session history is initialized if not present"""
# 		# Simulate session with no history
#         # with client.session_transaction() as sess:
#         #     sess.pop("history", None)
        
#         # response = client.post(
#         #     '/chat',
#         #     json={"message": "Test message"},
#         #     content_type='application/json'
#         # )
        
#         # assert response.status_code == 200
#         # with client.session_transaction() as sess:
#         #     print('=========>', sess)
#         #     assert "history" in sess
#         #     assert len(sess["history"]) == 2
    
#     def test_chat_api_response_format(self, client, sample_messages):
#         """Test that API response has the correct format"""
#         response = client.post(
#             '/chat',
#             json=sample_messages["valid_message"],
#             content_type='application/json'
#         )
        
#         data = json.loads(response.data)
#         assert isinstance(data, dict)
#         assert "reply" in data
#         assert isinstance(data["reply"], str)
    
#     def test_chat_multiple_requests_same_session(self, client):
#         """Test multiple chat requests maintain session continuity"""
#         messages = ["Hello", "How are you?", "What's the weather?"]
        
#         for i, msg in enumerate(messages):
#             response = client.post(
#                 '/chat',
#                 json={"message": msg},
#                 content_type='application/json'
#             )
#             assert response.status_code == 200
            
#             with client.session_transaction() as sess:
#                 history = sess.get("history", [])
#                 # Each message adds user + assistant response
#                 expected_length = (i + 1) * 2
#                 assert len(history) == expected_length
#                 assert history[-2]["role"] == "user"
#                 assert history[-2]["content"] == msg
    
#     def test_chat_content_type_validation(self, client):
#         """Test that wrong Content-Type is handled appropriately"""
#         response = client.post(
#             '/chat',
#             data="message=Hello",
#             content_type='application/x-www-form-urlencoded'
#         )
        
#         # Your endpoint may not support this content type
#         assert response.status_code in [400, 415]


# class TestClearEndpoint:
#     """Test suite for /clear endpoint"""
    
#     def test_clear_endpoint_success(self, client):
#         """Test successful session clearing"""
#         # First, add some history
#         client.post('/chat', json={"message": "Hello"})
        
#         # Verify history exists
#         with client.session_transaction() as sess:
#             assert len(sess.get("history", [])) > 0
        
#         # Clear the session
#         response = client.post('/clear')
        
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data["ok"] is True
        
#         # Verify history is cleared
#         with client.session_transaction() as sess:
#             assert sess.get("history", []) == []
    
#     def test_clear_empty_session(self, client):
#         """Test clearing an already empty session"""
#         response = client.post('/clear')
        
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data["ok"] is True
        
#         with client.session_transaction() as sess:
#             assert sess.get("history", []) == []
    
#     def test_clear_multiple_times(self, client):
#         """Test clearing session multiple times"""
#         # Add and clear multiple times
#         for _ in range(3):
#             client.post('/chat', json={"message": "Hello"})
#             response = client.post('/clear')
#             assert response.status_code == 200
            
#             with client.session_transaction() as sess:
#                 assert sess.get("history", []) == []
    
#     def test_clear_response_format(self, client):
#         """Test that clear endpoint returns correct response format"""
#         response = client.post('/clear')
        
#         data = json.loads(response.data)
#         assert isinstance(data, dict)
#         assert "ok" in data
#         assert data["ok"] is True
    
#     def test_clear_without_session(self, client):
#         """Test clear endpoint when no session exists"""
#         # Ensure session is fresh
#         with client.session_transaction() as sess:
#             sess.clear()
        
#         response = client.post('/clear')
#         assert response.status_code == 200
        
#         data = json.loads(response.data)
#         assert data["ok"] is True


# class TestSessionManagement:
#     """Test suite for session behavior across endpoints"""
    
#     def test_session_persistence_across_endpoints(self, client):
#         """Test that session persists across multiple endpoint calls"""
#         # Chat to create history
#         client.post('/chat', json={"message": "Message 1"})
        
#         # Verify history from session
#         with client.session_transaction() as sess:
#             assert len(sess.get("history", [])) == 2
        
#         # Clear session
#         client.post('/clear')
        
#         # Verify history is gone
#         with client.session_transaction() as sess:
#             assert sess.get("history", []) == []
        
#         # Chat again to create new history
#         client.post('/chat', json={"message": "Message 2"})
        
#         with client.session_transaction() as sess:
#             history = sess.get("history", [])
#             assert len(history) == 2
#             assert history[0]["content"] == "Message 2"
    
# 	# @unittest.skip("")
#     # def test_independent_sessions(self, app):
#     #     """Test that different clients have independent sessions"""
#     #     with app.test_client() as client1:
#     #         with app.test_client() as client2:
#     #             # Client 1 sends a message
#     #             client1.post('/chat', json={"message": "Client 1"})
                
#     #             # Client 2 should have empty history
#     #             with client2.session_transaction() as sess2:
#     #                 assert sess2.get("history") is None or sess2.get("history") == []
                
#     #             # Client 2 sends its own message
#     #             client2.post('/chat', json={"message": "Client 2"})
                
#     #             # Histories should be independent
#     #             with client1.session_transaction() as sess1:
#     #                 assert len(sess1.get("history", [])) == 2
#     #             with client2.session_transaction() as sess2:
#     #                 assert len(sess2.get("history", [])) == 2


# class TestErrorHandling:
#     """Test suite for error handling scenarios"""
    
#     def test_chat_with_malformed_json(self, client, sample_messages):
#         """Test chat with malformed JSON body"""
#         response = client.post(
#             '/chat',
#             data=sample_messages["malformed_json"],
#             content_type='application/json'
#         )
        
#         assert response.status_code in [400, 500]
    
#     def test_chat_with_large_payload(self, client):
#         """Test chat with extremely large payload"""
#         large_message = {"message": "A" * 1000000}  # 1MB message
        
#         response = client.post(
#             '/chat',
#             json=large_message,
#             content_type='application/json'
#         )
        
#         # Should handle large payloads or return 413
#         assert response.status_code in [200, 413]
    
#     def test_chat_special_characters(self, client):
#         """Test chat with messages containing special characters"""
#         special_message = {"message": "Special chars: !@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"}
        
#         response = client.post(
#             '/chat',
#             json=special_message,
#             content_type='application/json'
#         )
        
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert "reply" in data


# class TestPerformance:
#     """Performance test suite (use with caution - may be slow)"""
#     @unittest.skip("")
#     @pytest.mark.slow
#     def test_concurrent_requests(self, client):
#         """Test handling multiple concurrent requests"""
#         import threading
#         import time
        
#         results = []
#         errors = []
        
#         def make_request():
#             try:
#                 response = client.post('/chat', json={"message": "Hello"})
#                 results.append(response.status_code)
#             except Exception as e:
#                 errors.append(str(e))
        
#         # Create multiple threads
#         threads = []
#         for _ in range(10):
#             thread = threading.Thread(target=make_request)
#             threads.append(thread)
#             thread.start()
        
#         # Wait for all threads to complete
#         for thread in threads:
#             thread.join()
        
#         # All requests should succeed
#         assert len(errors) == 0
#         assert all(code == 200 for code in results)
    
#     # @pytest.mark.slow
#     # def test_many_sequential_requests(self, client):
#     #     """Test performance with many sequential requests"""
#     #     start_time = time.time()
        
#     #     for i in range(50):
#     #         response = client.post('/chat', json={"message": f"Message {i}"})
#     #         assert response.status_code == 200
        
#     #     elapsed = time.time() - start_time
#     #     # Assert that 50 requests complete in reasonable time (adjust threshold)
#     #     assert elapsed < 10  # Less than 10 seconds for 50 requests