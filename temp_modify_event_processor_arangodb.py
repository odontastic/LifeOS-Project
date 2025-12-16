import re
import os

file_path = "apps/backend/lifeos-rag-api/src/event_sourcing/event_processor.py"

# New combined ArangoDB/ReadModel handlers to insert
new_arangodb_handlers_code = """
    # -- ArangoDB & ReadModel Combined Handlers (for Project) --
    async def _handle_project_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            project = ProjectReadModel(**payload)
            db.add(project)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("projects")
                await self.arangodb_service.upsert_vertex(
                    collection_name="projects",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ProjectCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_project_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(ProjectReadModel).filter(ProjectReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("projects")
                await self.arangodb_service.upsert_vertex(
                    collection_name="projects",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ProjectUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_project_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(ProjectReadModel).filter(ProjectReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="projects",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ProjectDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise
    
    # -- ArangoDB & ReadModel Combined Handlers (for Area) --
    async def _handle_area_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            area = AreaReadModel(**payload)
            db.add(area)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("areas")
                await self.arangodb_service.upsert_vertex(
                    collection_name="areas",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing AreaCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_area_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(AreaReadModel).filter(AreaReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("areas")
                await self.arangodb_service.upsert_vertex(
                    collection_name="areas",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing AreaUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_area_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(AreaReadModel).filter(AreaReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="areas",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing AreaDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Task) --
    async def _handle_task_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            task = TaskReadModel(**payload)
            db.add(task)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("tasks")
                await self.arangodb_service.upsert_vertex(
                    collection_name="tasks",
                    vertex_data=payload,
                    key=doc_id
                )
            # Handle potential edge for project relationship
            project_id = payload.get("project")
            if project_id and doc_id:
                await self.arangodb_service.create_collection_if_not_exists("contains", edge=True)
                await self.arangodb_service.upsert_edge(
                    collection_name="contains",
                    from_vertex_key=f"projects/{project_id}",
                    to_vertex_key=f"tasks/{doc_id}",
                    edge_data={"relation": "contains_task"}
                )
        except Exception as e:
            logger.error(f"Error processing TaskCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_task_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(TaskReadModel).filter(TaskReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("tasks")
                await self.arangodb_service.upsert_vertex(
                    collection_name="tasks",
                    vertex_data=payload,
                    key=doc_id
                )
            # Handle potential edge for project relationship
            project_id = payload.get("project")
            if project_id and doc_id:
                await self.arangodb_service.create_collection_if_not_exists("contains", edge=True)
                await self.arangodb_service.upsert_edge(
                    collection_name="contains",
                    from_vertex_key=f"projects/{project_id}",
                    to_vertex_key=f"tasks/{doc_id}",
                    edge_data={"relation": "contains_task"}
                )
            else: # If project is removed, ensure edge is deleted (this is a simple check, more robust needed for all edge cases)
                # This part is complex. For now, we'll focus on creation/update.
                # A full solution would query existing edges and delete if no longer present.
                pass
        except Exception as e:
            logger.error(f"Error processing TaskUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_task_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(TaskReadModel).filter(TaskReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="tasks",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing TaskDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise
    
    # -- ArangoDB & ReadModel Combined Handlers (for Goal) --
    async def _handle_goal_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            goal = GoalReadModel(**payload)
            db.add(goal)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("goals")
                await self.arangodb_service.upsert_vertex(
                    collection_name="goals",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing GoalCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_goal_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(GoalReadModel).filter(GoalReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("goals")
                await self.arangodb_service.upsert_vertex(
                    collection_name="goals",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing GoalUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_goal_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(GoalReadModel).filter(GoalReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="goals",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing GoalDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Reflection) --
    async def _handle_reflection_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            reflection = ReflectionReadModel(**payload)
            db.add(reflection)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("reflections")
                await self.arangodb_service.upsert_vertex(
                    collection_name="reflections",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ReflectionCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_reflection_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("reflections")
                await self.arangodb_service.upsert_vertex(
                    collection_name="reflections",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ReflectionUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_reflection_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(ReflectionReadModel).filter(ReflectionReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="reflections",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing ReflectionDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Journal Entry) --
    async def _handle_journal_entry_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            journal_entry = JournalEntryReadModel(**payload)
            db.add(journal_entry)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("journal_entries")
                await self.arangodb_service.upsert_vertex(
                    collection_name="journal_entries",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing JournalEntryCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_journal_entry_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("journal_entries")
                await self.arangodb_service.upsert_vertex(
                    collection_name="journal_entries",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing JournalEntryUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_journal_entry_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(JournalEntryReadModel).filter(JournalEntryReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="journal_entries",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing JournalEntryDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Emotion) --
    async def _handle_emotion_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            emotion = EmotionReadModel(**payload)
            db.add(emotion)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("emotions")
                await self.arangodb_service.upsert_vertex(
                    collection_name="emotions",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing EmotionCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_emotion_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(EmotionReadModel).filter(EmotionReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("emotions")
                await self.arangodb_service.upsert_vertex(
                    collection_name="emotions",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing EmotionUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_emotion_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(EmotionReadModel).filter(EmotionReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="emotions",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing EmotionDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Belief) --
    async def _handle_belief_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            belief = BeliefReadModel(**payload)
            db.add(belief)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("beliefs")
                await self.arangodb_service.upsert_vertex(
                    collection_name="beliefs",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing BeliefCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_belief_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(BeliefReadModel).filter(BeliefReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("beliefs")
                await self.arangodb_service.upsert_vertex(
                    collection_name="beliefs",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing BeliefUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_belief_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(BeliefReadModel).filter(BeliefReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="beliefs",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing BeliefDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    # -- ArangoDB & ReadModel Combined Handlers (for Trigger) --
    async def _handle_trigger_created_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            trigger = TriggerReadModel(**payload)
            db.add(trigger)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("triggers")
                await self.arangodb_service.upsert_vertex(
                    collection_name="triggers",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing TriggerCreated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_trigger_updated_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel update
            payload_converted = EventProcessor._convert_str_to_datetime(payload)
            db.query(TriggerReadModel).filter(TriggerReadModel.id == payload_converted["id"]).update(payload_converted)

            # Update ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.create_collection_if_not_exists("triggers")
                await self.arangodb_service.upsert_vertex(
                    collection_name="triggers",
                    vertex_data=payload,
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing TriggerUpdated event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise

    async def _handle_trigger_deleted_arangodb_and_readmodel(self, db: Session, payload: Dict[str, Any]):
        try:
            # Handle ReadModel delete
            db.query(TriggerReadModel).filter(TriggerReadModel.id == payload["id"]).delete()

            # Delete from ArangoDB
            doc_id = payload.get("id")
            if doc_id:
                await self.arangodb_service.delete_vertex(
                    collection_name="triggers",
                    key=doc_id
                )
        except Exception as e:
            logger.error(f"Error processing TriggerDeleted event for ArangoDB (payload: {payload}): {e}", exc_info=True)
            raise