from strands.tools import tool

# MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
MODEL_ID = "amazon.nova-micro-v1:0"

# System prompt defining the agent's role and capabilities
SYSTEM_PROMPT = """You are an intelligent learning tracker assistant for personal skill development.

Your role is to:
- Help users track their learning progress across different topics
- Remember user learning preferences (content format: videos vs documents, learning pace)
- Understand their current knowledge level and learning goals
- Provide personalized learning recommendations based on history
- Summarize what's been covered and suggest next steps
- Be encouraging and supportive in learning journey

You have access to the following tools:
1. add_topic() - Add a new topic to the learning track
2. record_progress() - Record progress on a specific topic (include subtopics, concepts learned)
3. get_learning_status() - Check current learning status and progress
4. get_topic_recommendations() - Get personalized topic recommendations based on preferences
5. update_learning_preference() - Update learning preferences (pace and content format)

Always use the appropriate tool to help users track and manage their learning journey effectively."""


@tool
def add_topic(topic_name: str, description: str = None, category: str = None) -> str:
    """
    Add a new topic to the learning tracker.
    
    Args:
        topic_name: Name of the topic (e.g., "Kubernetes", "Python Async")
        description: Brief description of what to learn
        category: Category of the topic (e.g., "DevOps", "Programming", "Cloud")
    
    Returns:
        Confirmation of topic addition
    """
    print(f"topic_name = {topic_name}")
    print(f"description = {description}")
    print(f"category = {category}")
    
    # Mock database of topics
    topics_db = {
        "Kubernetes": {
            "category": "DevOps",
            "description": "Container orchestration platform",
            "subtopics": ["Pods", "Services", "Deployments", "StatefulSets"]
        },
        "Docker": {
            "category": "DevOps", 
            "description": "Containerization platform",
            "subtopics": ["Images", "Containers", "Networks", "Volumes"]
        },
        "Python Async": {
            "category": "Programming",
            "description": "Asynchronous programming in Python",
            "subtopics": ["async/await", "Event Loop", "Coroutines", "Tasks"]
        },
        "React": {
            "category": "Frontend",
            "description": "React framework for UI development",
            "subtopics": ["Components", "Hooks", "State Management", "Routing"]
        },
        "GraphQL": {
            "category": "Backend",
            "description": "Query language for APIs",
            "subtopics": ["Queries", "Mutations", "Subscriptions", "Schema"]
        }
    }
    
    if topic_name in topics_db:
        topic_info = topics_db[topic_name]
        return f"""✅ Added '{topic_name}' to your learning track!

Category: {topic_info['category']}
Description: {topic_info['description']}

Key subtopics to cover:
{chr(10).join(f"  • {st}" for st in topic_info['subtopics'])}

I'll remember this and help you track your progress."""
    else:
        return f"""✅ Added '{topic_name}' to your learning track!

I've created a new topic. As you study, I'll help you track:
  • Subtopics covered
  • Concepts learned
  • Your learning pace
  • Preferred content format (videos/docs)

Let me know when you've made progress!"""


@tool
def record_progress(topic_name: str, subtopics_covered: str = None, concepts_learned: str = None, hours_spent: float = None) -> str:
    """
    Record progress on a specific topic.
    
    Args:
        topic_name: Name of the topic
        subtopics_covered: Comma-separated list of subtopics completed
        concepts_learned: Key concepts learned (comma-separated)
        hours_spent: Hours spent on this topic/session
    
    Returns:
        Confirmation of progress recording
    """
    print(f"topic_name = {topic_name}")
    print(f"subtopics_covered = {subtopics_covered}")
    print(f"concepts_learned = {concepts_learned}")
    print(f"hours_spent = {hours_spent}")
    
    response = f"✅ Progress recorded for '{topic_name}'!\n\n"
    
    if subtopics_covered:
        response += f"📚 Subtopics Covered:\n"
        for subtopic in subtopics_covered.split(","):
            response += f"  ✓ {subtopic.strip()}\n"
    
    if concepts_learned:
        response += f"\n🧠 Concepts Learned:\n"
        for concept in concepts_learned.split(","):
            response += f"  • {concept.strip()}\n"
    
    if hours_spent:
        response += f"\n⏱️ Time Invested: {hours_spent} hours\n"
    
    response += f"\n🎯 I'm tracking your progress and will remember this for next session!"
    
    return response


@tool
def get_learning_status(topic_name: str = None) -> str:
    """
    Check current learning status and progress.
    
    Args:
        topic_name: Optional specific topic. If not provided, returns all topics
    
    Returns:
        Summary of learning progress
    """
    print(f"topic_name = {topic_name}")
    
    # Mock learning progress data
    progress_db = {
        "Kubernetes": {
            "status": "In Progress",
            "progress": "45%",
            "covered": ["Pods", "Services"],
            "next": ["Deployments", "StatefulSets"],
            "hours_invested": 12.5,
            "last_session": "2 days ago"
        },
        "Docker": {
            "status": "Completed",
            "progress": "100%",
            "covered": ["Images", "Containers", "Networks", "Volumes"],
            "hours_invested": 8,
            "completed_date": "1 week ago"
        },
        "Python Async": {
            "status": "Not Started",
            "progress": "0%",
            "hours_invested": 0
        }
    }
    
    if topic_name:
        if topic_name in progress_db:
            info = progress_db[topic_name]
            response = f"📊 Learning Status: {topic_name}\n\n"
            response += f"Status: {info['status']}\n"
            response += f"Progress: {info['progress']}\n"
            
            if info.get('covered'):
                response += f"\n✅ Covered:\n"
                for item in info['covered']:
                    response += f"  • {item}\n"
            
            if info.get('next'):
                response += f"\n→ Next:\n"
                for item in info['next']:
                    response += f"  • {item}\n"
            
            response += f"\n⏱️ Hours Invested: {info['hours_invested']}\n"
            
            if info.get('last_session'):
                response += f"Last Session: {info['last_session']}\n"
            
            return response
        else:
            return f"No progress data found for '{topic_name}'. Start tracking by recording your first session!"
    else:
        response = "📚 Your Learning Overview:\n\n"
        for topic, info in progress_db.items():
            response += f"• {topic}: {info['progress']} - {info['status']}\n"
        return response


@tool
def get_topic_recommendations(learning_goal: str = None) -> str:
    """
    Get personalized topic recommendations based on learning preferences and goals.
    
    Args:
        learning_goal: Optional learning goal (e.g., "backend development", "DevOps")
    
    Returns:
        Personalized recommendations
    """
    print(f"learning_goal = {learning_goal}")
    
    # Mock recommendation engine
    recommendations = {
        "DevOps": [
            {"topic": "Docker", "reason": "Foundation for containerization", "estimated_hours": 8},
            {"topic": "Kubernetes", "reason": "Next step after Docker mastery", "estimated_hours": 20},
            {"topic": "Terraform", "reason": "Infrastructure as Code", "estimated_hours": 15}
        ],
        "Backend": [
            {"topic": "Python Async", "reason": "Build scalable services", "estimated_hours": 12},
            {"topic": "GraphQL", "reason": "Modern API development", "estimated_hours": 16},
            {"topic": "Database Design", "reason": "Critical for backends", "estimated_hours": 18}
        ],
        "Frontend": [
            {"topic": "React", "reason": "Most popular framework", "estimated_hours": 24},
            {"topic": "TypeScript", "reason": "Type safety in projects", "estimated_hours": 14},
            {"topic": "CSS Grid & Flexbox", "reason": "Modern layout techniques", "estimated_hours": 10}
        ]
    }
    
    if learning_goal:
        goal_lower = learning_goal.lower()
        for key in recommendations:
            if key.lower() in goal_lower or goal_lower in key.lower():
                response = f"🎯 Recommended Learning Path for {key}:\n\n"
                for i, rec in enumerate(recommendations[key], 1):
                    response += f"{i}. {rec['topic']}\n"
                    response += f"   Reason: {rec['reason']}\n"
                    response += f"   Estimated: {rec['estimated_hours']} hours\n\n"
                return response
        
        return f"I'll recommend topics based on your learning journey and preferences!"
    else:
        response = "🌟 Popular Learning Paths:\n\n"
        for path in recommendations:
            response += f"• {path}\n"
        return response


@tool
def update_learning_preference(content_format: str = None, learning_pace: str = None) -> str:
    """
    Update learning preferences for personalized recommendations.
    
    Args:
        content_format: Preferred format ('videos', 'documentation', 'mixed')
        learning_pace: Preferred pace ('slow', 'moderate', 'fast')
    
    Returns:
        Confirmation of preference update
    """
    print(f"content_format = {content_format}")
    print(f"learning_pace = {learning_pace}")
    
    response = "✅ Updated your learning preferences!\n\n"
    
    if content_format:
        response += f"📺 Content Format: {content_format}\n"
        if content_format.lower() == "videos":
            response += "   I'll prioritize video tutorials and visual explanations\n"
        elif content_format.lower() == "documentation":
            response += "   I'll focus on official docs and written guides\n"
        elif content_format.lower() == "mixed":
            response += "   I'll suggest a mix of videos and documentation\n"
    
    if learning_pace:
        response += f"\n⚡ Learning Pace: {learning_pace}\n"
        if learning_pace.lower() == "slow":
            response += "   I'll provide detailed explanations and pace recommendations\n"
        elif learning_pace.lower() == "moderate":
            response += "   Balanced depth and speed in recommendations\n"
        elif learning_pace.lower() == "fast":
            response += "   I'll suggest advanced topics and focus on key concepts\n"
    
    response += "\n🎓 I'll use these preferences for all future recommendations!"
    
    return response


print("✅ Learning tracker tools ready")
