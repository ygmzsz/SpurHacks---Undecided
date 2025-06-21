import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  TextInput,
  Modal,
  Alert,
  SafeAreaView,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface Event {
  id: string;
  title: string;
  time: string;
  description: string;
}

interface Events {
  [key: string]: Event[];
}

const WeeklyPlannerScreen: React.FC = () => {
  const [currentDate, setCurrentDate] = useState<Date>(new Date());
  const [events, setEvents] = useState<Events>({});
  const [modalVisible, setModalVisible] = useState<boolean>(false);
  const [selectedDate, setSelectedDate] = useState<string>('');
  const [eventTitle, setEventTitle] = useState<string>('');
  const [eventTime, setEventTime] = useState<string>('');
  const [eventDescription, setEventDescription] = useState<string>('');

  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  // Get current week dates
  const getCurrentWeekDates = (): Date[] => {
    const week: Date[] = [];
    const startOfWeek = new Date(currentDate);
    const day = startOfWeek.getDay();
    const diff = startOfWeek.getDate() - day;
    startOfWeek.setDate(diff);

    for (let i = 0; i < 7; i++) {
      const date = new Date(startOfWeek);
      date.setDate(startOfWeek.getDate() + i);
      week.push(date);
    }
    return week;
  };

  const formatDateKey = (date: Date): string => {
    return date.toISOString().split('T')[0];
  };

  const addEvent = (): void => {
    if (!eventTitle.trim()) {
      Alert.alert('Error', 'Please enter an event title');
      return;
    }

    const eventKey = formatDateKey(new Date(selectedDate));
    const newEvent: Event = {
      id: Date.now().toString(),
      title: eventTitle,
      time: eventTime,
      description: eventDescription,
    };

    setEvents(prev => ({
      ...prev,
      [eventKey]: [...(prev[eventKey] || []), newEvent]
    }));

    // Clear form
    setEventTitle('');
    setEventTime('');
    setEventDescription('');
    setModalVisible(false);
  };

  const deleteEvent = (dateKey: string, eventId: string): void => {
    setEvents(prev => ({
      ...prev,
      [dateKey]: prev[dateKey].filter(event => event.id !== eventId)
    }));
  };

  const navigateWeek = (direction: number): void => {
    const newDate = new Date(currentDate);
    newDate.setDate(currentDate.getDate() + (direction * 7));
    setCurrentDate(newDate);
  };

  const openAddEventModal = (date: Date): void => {
    setSelectedDate(date.toISOString());
    setModalVisible(true);
  };

  const weekDates = getCurrentWeekDates();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#fff" />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigateWeek(-1)}>
          <Ionicons name="chevron-back" size={24} color="#007AFF" />
        </TouchableOpacity>
        
        <Text style={styles.headerTitle}>
          {months[currentDate.getMonth()]} {currentDate.getFullYear()}
        </Text>
        
        <TouchableOpacity onPress={() => navigateWeek(1)}>
          <Ionicons name="chevron-forward" size={24} color="#007AFF" />
        </TouchableOpacity>
      </View>

      {/* Week View */}
      <ScrollView style={styles.content}>
        {weekDates.map((date, index) => {
          const dateKey = formatDateKey(date);
          const dayEvents = events[dateKey] || [];
          const isToday = new Date().toDateString() === date.toDateString();

          return (
            <View key={index} style={styles.dayContainer}>
              <View style={[styles.dayHeader, isToday && styles.todayHeader]}>
                <Text style={[styles.dayName, isToday && styles.todayText]}>
                  {daysOfWeek[date.getDay()]}
                </Text>
                <Text style={[styles.dayNumber, isToday && styles.todayText]}>
                  {date.getDate()}
                </Text>
                <TouchableOpacity
                  style={styles.addButton}
                  onPress={() => openAddEventModal(date)}
                >
                  <Ionicons name="add" size={20} color={isToday ? "#fff" : "#007AFF"} />
                </TouchableOpacity>
              </View>

              <View style={styles.eventsContainer}>
                {dayEvents.length === 0 ? (
                  <Text style={styles.noEventsText}>No events scheduled</Text>
                ) : (
                  dayEvents.map((event) => (
                    <View key={event.id} style={styles.eventCard}>
                      <View style={styles.eventContent}>
                        <Text style={styles.eventTitle}>{event.title}</Text>
                        {event.time && (
                          <Text style={styles.eventTime}>{event.time}</Text>
                        )}
                        {event.description && (
                          <Text style={styles.eventDescription}>{event.description}</Text>
                        )}
                      </View>
                      <TouchableOpacity
                        style={styles.deleteButton}
                        onPress={() => deleteEvent(dateKey, event.id)}
                      >
                        <Ionicons name="trash-outline" size={16} color="#FF3B30" />
                      </TouchableOpacity>
                    </View>
                  ))
                )}
              </View>
            </View>
          );
        })}
      </ScrollView>

      {/* Add Event Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Add New Event</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close" size={24} color="#666" />
              </TouchableOpacity>
            </View>

            <View style={styles.formContainer}>
              <Text style={styles.inputLabel}>Event Title *</Text>
              <TextInput
                style={styles.textInput}
                value={eventTitle}
                onChangeText={setEventTitle}
                placeholder="Enter event title"
                placeholderTextColor="#999"
              />

              <Text style={styles.inputLabel}>Time</Text>
              <TextInput
                style={styles.textInput}
                value={eventTime}
                onChangeText={setEventTime}
                placeholder="e.g., 9:00 AM"
                placeholderTextColor="#999"
              />

              <Text style={styles.inputLabel}>Description</Text>
              <TextInput
                style={[styles.textInput, styles.textArea]}
                value={eventDescription}
                onChangeText={setEventDescription}
                placeholder="Event description (optional)"
                placeholderTextColor="#999"
                multiline
                numberOfLines={3}
              />

              <View style={styles.buttonContainer}>
                <TouchableOpacity
                  style={[styles.button, styles.cancelButton]}
                  onPress={() => setModalVisible(false)}
                >
                  <Text style={styles.cancelButtonText}>Cancel</Text>
                </TouchableOpacity>
                
                <TouchableOpacity
                  style={[styles.button, styles.saveButton]}
                  onPress={addEvent}
                >
                  <Text style={styles.saveButtonText}>Save Event</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#333',
  },
  content: {
    flex: 1,
    paddingHorizontal: 16,
    paddingTop: 10,
  },
  dayContainer: {
    marginBottom: 20,
    backgroundColor: '#fff',
    borderRadius: 12,
    overflow: 'hidden',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  dayHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#f8f9fa',
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  todayHeader: {
    backgroundColor: '#007AFF',
  },
  dayName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    minWidth: 40,
  },
  dayNumber: {
    fontSize: 16,
    fontWeight: '500',
    color: '#666',
    marginLeft: 8,
    minWidth: 30,
  },
  todayText: {
    color: '#fff',
  },
  addButton: {
    marginLeft: 'auto',
    padding: 4,
  },
  eventsContainer: {
    padding: 16,
  },
  noEventsText: {
    color: '#999',
    fontStyle: 'italic',
    textAlign: 'center',
    paddingVertical: 20,
  },
  eventCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#007AFF',
  },
  eventContent: {
    flex: 1,
  },
  eventTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  eventTime: {
    fontSize: 14,
    color: '#007AFF',
    fontWeight: '500',
    marginBottom: 4,
  },
  eventDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  deleteButton: {
    padding: 4,
    marginLeft: 8,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    paddingBottom: 34,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
  },
  formContainer: {
    padding: 20,
  },
  inputLabel: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
    marginBottom: 8,
    marginTop: 16,
  },
  textInput: {
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#fff',
  },
  textArea: {
    height: 80,
    textAlignVertical: 'top',
  },
  buttonContainer: {
    flexDirection: 'row',
    marginTop: 24,
    gap: 12,
  },
  button: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  saveButton: {
    backgroundColor: '#007AFF',
  },
  cancelButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
  },
  saveButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
});

export default WeeklyPlannerScreen;