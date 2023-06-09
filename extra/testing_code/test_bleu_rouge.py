from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge

def get_bleu_and_rouge(reference: str, generated: str):
    reference_tokens = reference.split()
    generated_tokens = generated.split()
    smoothie = SmoothingFunction().method4
    bleu_score = sentence_bleu([reference_tokens], generated_tokens, smoothing_function=smoothie)
    rouge = Rouge()
    rouge_scores = rouge.get_scores(generated, reference, avg=True)
    
    rouge_f1_scores = {
        "rouge-1": rouge_scores["rouge-1"]["f"],
        "rouge-2": rouge_scores["rouge-2"]["f"],
        "rouge-l": rouge_scores["rouge-l"]["f"],
    }
    return bleu_score, rouge_f1_scores

# Example usage
reference = "COVID   Good guidelines can be found at cdc.  gov/coronavirus/2019.  You would be considered low risk. Symptoms last up to two weeks. High probability many will get the disease and testing leads to no change in action at this time.  No obvious therapy (however some encouraging possibilites) and for most people the virus runs its course without incidence. Stay put and talk to your provider.   Would you like to video or text chat with me?"
generated = "Hard to guess. You have some of the  symptoms of cold , flu and covid19 . Also you appear to be dehydrated. But you are young and no mention of any underlying medical condition. So, i  think you are not vulnerable.  Drink at least 6 cups of water a day. Probably need self isolation for 2 weeks and to be tested in mean time for covid19 if you develop breathing problem. Contact to your doctor for a guidance."

bleu_score, rouge_f1_scores = get_bleu_and_rouge(reference, generated)
print("BLEU Score:", bleu_score)
print("ROUGE F1 Scores:", rouge_f1_scores)