       # --- Query Methods ---
       def get_read_model(self, model_type: Type[Base], item_id: str) ->
   Optional[Dict[str, Any]]:
           with self._get_db() as db:
               item = db.query(model_type).filter(model_type.id == item_id).first()
               if item:
                   return item.__dict__
               return None

       def get_all_read_models(self, model_type: Type[Base]) -> List[Dict[str, Any]]:
           with self._get_db() as db:
               items = db.query(model_type).all()
               return [item.__dict__ for item in items]
