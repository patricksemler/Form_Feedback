import { useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import * as ImagePicker from 'expo-image-picker';

export default function HomeScreen() {
    const [videoURI, setVideoURI] = useState<string | null>(null);

    enum Exercise {
        PUSHUP = "pushup",
        SITUP = "situp",
        SQUAT = "squat",
        LUNGE = "lunge",
    };

    const [selectedExercise, setSelectedExercise] = useState(Exercise.PUSHUP);

    async function pickVideo() {
        const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();

        if (status !== 'granted') {
            alert('Media library permissions not granted.')
            return;
        }

        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Videos,
            allowsEditing: false,
            quality: 0.5,
        });

        if (!result.canceled) {
            setVideoURI(result.assets[0].uri);
            console.log(`Picked video URI: ${videoURI}`)
        }
    }

    return (
        <View style={styles.container}>
            <Text style={styles.title}>🏠 Home Screen</Text>
            <Text style={styles.paragraph}>Welcome to Form Feedback</Text>

            <Picker
                selectedValue={selectedExercise}
                onValueChange={(itemValue) => {
                    setSelectedExercise(itemValue as Exercise);
                }}
            >
                <Picker.Item label="Push Up" value={Exercise.PUSHUP} />
                <Picker.Item label="Sit Up" value={Exercise.SITUP} />
                <Picker.Item label="Squat" value={Exercise.SQUAT} />
                <Picker.Item label="Lunge" value={Exercise.LUNGE} />
            </Picker>
            <Button title="Upload Video" onPress={pickVideo} />
            {videoURI && (
                <Text style={styles.paragraph}>Selected video: {videoURI}</Text>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    paragraph: {
        fontSize: 18,
        marginBottom: 10,
    },
});
