// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME dOdictdITRadCorDict

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "TRadCor.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static TClass *TRadCor_Dictionary();
   static void TRadCor_TClassManip(TClass*);
   static void *new_TRadCor(void *p = 0);
   static void *newArray_TRadCor(Long_t size, void *p);
   static void delete_TRadCor(void *p);
   static void deleteArray_TRadCor(void *p);
   static void destruct_TRadCor(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TRadCor*)
   {
      ::TRadCor *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::TRadCor));
      static ::ROOT::TGenericClassInfo 
         instance("TRadCor", "TRadCor.h", 11,
                  typeid(::TRadCor), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &TRadCor_Dictionary, isa_proxy, 0,
                  sizeof(::TRadCor) );
      instance.SetNew(&new_TRadCor);
      instance.SetNewArray(&newArray_TRadCor);
      instance.SetDelete(&delete_TRadCor);
      instance.SetDeleteArray(&deleteArray_TRadCor);
      instance.SetDestructor(&destruct_TRadCor);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TRadCor*)
   {
      return GenerateInitInstanceLocal((::TRadCor*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TRadCor*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *TRadCor_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::TRadCor*)0x0)->GetClass();
      TRadCor_TClassManip(theClass);
   return theClass;
   }

   static void TRadCor_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_TRadCor(void *p) {
      return  p ? new(p) ::TRadCor : new ::TRadCor;
   }
   static void *newArray_TRadCor(Long_t nElements, void *p) {
      return p ? new(p) ::TRadCor[nElements] : new ::TRadCor[nElements];
   }
   // Wrapper around operator delete
   static void delete_TRadCor(void *p) {
      delete ((::TRadCor*)p);
   }
   static void deleteArray_TRadCor(void *p) {
      delete [] ((::TRadCor*)p);
   }
   static void destruct_TRadCor(void *p) {
      typedef ::TRadCor current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TRadCor

namespace {
  void TriggerDictionaryInitialization_TRadCorDict_Impl() {
    static const char* headers[] = {
"TRadCor.h",
0
    };
    static const char* includePaths[] = {
"/home/matias/software/safe/construir/include",
"/home/matias/proyecto/TwoPionAnalysis/RCFactor/HAPRAD_CPP/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "TRadCorDict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$TRadCor.h")))  TRadCor;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "TRadCorDict dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
#include "TRadCor.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"TRadCor", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("TRadCorDict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_TRadCorDict_Impl, {}, classesHeaders);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_TRadCorDict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_TRadCorDict() {
  TriggerDictionaryInitialization_TRadCorDict_Impl();
}
