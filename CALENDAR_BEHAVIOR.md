# Calendar Behavior

## Current Implementation

The calendar **automatically advances each day**.

### How it works:
- The calendar always displays **14 days starting from TODAY**
- It uses `datetime.now().date()` as the starting point
- Each day, the calendar automatically shifts forward

### Example:
- **Wednesday, Oct 2**: Shows Oct 2 - Oct 15
- **Thursday, Oct 3**: Shows Oct 3 - Oct 16
- **Friday, Oct 4**: Shows Oct 4 - Oct 17

### Key Features:
1. **Rolling Window**: Always shows "today + 13 days ahead"
2. **No Past Dates**: Previous days automatically disappear
3. **Consistent View**: Users always see the next 2 weeks
4. **Today Highlighting**: The current day is highlighted with a purple gradient

### Code Location:
```python
def get_two_week_dates():
    """Get dates for the next 2 weeks from today"""
    dates = []
    start_date = datetime.now().date()  # ← Automatically uses TODAY
    
    for i in range(14):
        date = start_date + timedelta(days=i)
        dates.append(date)
    
    return dates
```

## Benefits:
- ✅ Users can't book slots in the past
- ✅ Calendar stays relevant and up-to-date
- ✅ No manual refresh needed
- ✅ "Today" marker always accurate
- ✅ Simple, predictable behavior

## Future Enhancements (Optional):
If needed, we could add:
- Date range selector (e.g., view weeks 3-4 ahead)
- Month view option
- Calendar jump-to-date feature

