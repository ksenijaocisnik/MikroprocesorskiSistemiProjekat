from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from values import IMAGE_HEIGHT, IMAGE_WIDTH, COLOR_COUNT

# Kreiranje modela 
# klasifikacija: binarna (FIRE/NO_FIRE)

def create_model(input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, COLOR_COUNT)):

    # Uctivanje pre-treined ResNet50V2 model koji je treniran na imagenet dateset-u
    # Potrebno je da dodamo nove slojeve i da ne menjamo one koji su vec odredjeni (u nasem projektu: FIRE/NO_FIRE)
    base_model = ResNet50V2(weights='resnet50v2_weights_tf_dim_ordering_tf_kernels_notop.h5', include_top=False, input_shape=input_shape)
    base_model.trainable = False 

    # Potrebno je da nadogradimo output pre-trained modela 
    base_model_output = base_model.output
    pooled_output = GlobalAveragePooling2D()(base_model_output)
    # Koristimo 1 neuron, jer je klasifikacija binarna i verovatnocu pozara predstavljamo sigmoid funkcijom koja 
    #   verovatnocu preslikava u broj izmedju 0 i 1 :
    #       ako je blize 1 -> NO_FIRE
    #       ako je blize 0 -> FIRE
    output = Dense(1, activation='sigmoid')(pooled_output)

    # Potrebno je da spojimo ono sto model vec zna sa slojevima koje smo mi dodali 
    model = Model(inputs=base_model.input, outputs=output)
    # Kompajliramo model, gde kvalitet modela merimo po tacnosti
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model
