# Acoustic Scene Analysis on Songbirds
This project investigates auditory scene analysis in songbirds — the ability to segregate and identify individual vocal signals within complex acoustic environments, akin to the human “cocktail party problem.” By creating a controlled acoustic setup that enables simultaneous recording of multiple vocalizing birds, we aim to study how spatial and spectral cues contribute to source separation, communication, and perception in naturalistic group settings.

### Microphone Directivity and Polar Pattern
To accurately capture and localize vocalizations within the recording space, it is essential to characterize the directional response of the microphones used. The cardioid microphone exhibits a polar pickup pattern that emphasizes sounds originating from the front while attenuating those from the sides and rear. This directional sensitivity helps reduce interference from neighboring sound sources and room reflections — a critical feature when multiple birds vocalize simultaneously. The following polar diagram illustrates the typical response pattern of the cardioid microphone employed in this study, highlighting its angular sensitivity across different frequencies. Mathematically, its polar response follows: 

$P(\theta) = 0.5 \times (1 + \cos\theta)$,

where $\theta$ is the angle between the mic’s forward axis and the direction of the incoming sound.

![mic](cardioid.png)
