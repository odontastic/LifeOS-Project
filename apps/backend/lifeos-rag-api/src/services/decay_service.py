import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from typing import List

from database import SystemInsightModel
from schemas import SystemInsight, InsightDecayedEvent
from event_bus import event_bus

logger = logging.getLogger(__name__)

def calculate_decay_status(insight: SystemInsight) -> float:
    """
    Calculates the current decay status of an insight as a float between 0.0 (fresh) and 1.0 (fully decayed).
    """
    if not insight.half_life_days or not insight.decay_start_date:
        return 0.0 # No decay configured

    current_time = datetime.now(timezone.utc)
    # Use last_reaffirmed_date if available, otherwise decay_start_date
    start_point = insight.last_reaffirmed_date if insight.last_reaffirmed_date else insight.decay_start_date

    time_since_start = current_time - start_point
    
    # Calculate decay based on half-life model
    # A simplified model: after N half-lives, consider it fully decayed.
    # For example, after 5 half-lives, remaining value is ~3.125%
    half_lives_passed = time_since_start.total_seconds() / (insight.half_life_days * 24 * 3600)
    
    # Max decay status at 1.0
    # Let's say after 5 half-lives, it's considered fully decayed (decay_status = 1.0)
    # So decay_status = min(1.0, half_lives_passed / 5.0)
    # This is a linear approximation of exponential decay for simplicity in status reporting
    decay_status = min(1.0, half_lives_passed / 5.0) 
    
    return decay_status

def process_decay_for_insights(db: Session):
    """
    Scans for insights that have decayed and emits InsightDecayedEvent.
    """
    logger.info("Running insight decay processing...")
    insights: List[SystemInsightModel] = db.query(SystemInsightModel).all()

    for insight_model in insights:
        # Convert SQLAlchemy model to Pydantic model for consistent schema access
        insight = SystemInsight.model_validate(insight_model.__dict__)

        decay_status = calculate_decay_status(insight)

        if decay_status >= 1.0: # Fully decayed
            logger.info(f"Insight {insight.id} has fully decayed. Emitting InsightDecayedEvent.")
            decay_event = InsightDecayedEvent(
                insight_id=insight.id,
                decay_status=decay_status,
                timestamp=datetime.now(timezone.utc)
            )
            # Emit the event; event_processor will handle the actual dissolution
            event_bus.emit(
                event_type="InsightDecayed", 
                payload=decay_event, 
                schema_version="1.0"
            )
        elif decay_status > 0: # Partially decayed, might log for monitoring
            logger.debug(f"Insight {insight.id} is partially decayed: {decay_status:.2f}")

    logger.info("Insight decay processing completed.")

if __name__ == "__main__":
    # This block is for testing the decay logic independently
    # In a real application, this would be scheduled by a background task runner.
    from database import SessionLocal, Base, engine
    Base.metadata.create_all(bind=engine) # Ensure tables are created

    # Example usage:
    db = SessionLocal()
    try:
        # Create a dummy insight for testing
        dummy_insight = SystemInsightModel(
            id=uuid.uuid4(),
            insight_type="test_decay",
            generated_from="[]",
            model_version="1.0",
            confidence=100,
            message="This is a test insight for decay.",
            half_life_days=1, # 1 day half-life
            decay_start_date=datetime.now(timezone.utc) - timedelta(days=5), # 5 days ago
            last_reaffirmed_date=None
        )
        db.add(dummy_insight)
        db.commit()
        db.refresh(dummy_insight)
        
        print(f"Created dummy insight: {dummy_insight.id}")
        process_decay_for_insights(db)

        # Another insight that should not be fully decayed yet
        dummy_insight_2 = SystemInsightModel(
            id=uuid.uuid4(),
            insight_type="test_decay_partial",
            generated_from="[]",
            model_version="1.0",
            confidence=100,
            message="This is a partially decayed test insight.",
            half_life_days=1,
            decay_start_date=datetime.now(timezone.utc) - timedelta(hours=12), # 12 hours ago
            last_reaffirmed_date=None
        )
        db.add(dummy_insight_2)
        db.commit()
        db.refresh(dummy_insight_2)
        
        print(f"Created dummy insight 2: {dummy_insight_2.id}")
        process_decay_for_insights(db)

    finally:
        db.close()
