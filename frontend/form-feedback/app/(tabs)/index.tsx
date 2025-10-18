import { Picker } from '@react-native-picker/picker';
import * as ImagePicker from 'expo-image-picker';
import { useState } from 'react';
import { Button, StyleSheet, Text, View } from 'react-native';

export default function HomeScreen() {
    const [videoURI, setVideoURI] = useState<string | null>(null);
    const [uploading, setUploading] = useState(false);

    enum Exercise {
        PUSHUP = 'pushup',
        SITUP = 'situp',
        SQUAT = 'squat',
        LUNGE = 'lunge',
    };

    const [selectedExercise, setSelectedExercise] = useState(Exercise.PUSHUP);

    async function pickAndUploadVideo() {
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
            console.log('Picked video URI:', videoURI)
        }

        const formData = new FormData();

        formData.append('exercise', selectedExercise);
        formData.append('video', {
            uri: videoURI,
            type: 'video/mp4',
            name: `${Date.now()}.mp4`,
        } as any);

        setUploading(true);

        try {
            const response = await fetch('(INSERT API URL HERE)', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText);
            }

            console.log(`Upload succeeded`);
        } catch (error) {
            console.log('Error:', error);
            alert('Upload failed.')
        } finally {
            setUploading(false);
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
                <Picker.Item label='Push Up' value={Exercise.PUSHUP} />
                <Picker.Item label='Sit Up' value={Exercise.SITUP} />
                <Picker.Item label='Squat' value={Exercise.SQUAT} />
                <Picker.Item label='Lunge' value={Exercise.LUNGE} />
            </Picker>
            <Button title='Upload Video' onPress={pickAndUploadVideo} />
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
