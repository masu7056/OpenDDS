#include "idl_defines.h"
#ifdef TAO_IDL_HAS_ANNOTATIONS
#ifndef SAMPLE_KEYS_HEADER
#define SAMPLE_KEYS_HEADER

#include <string>
#include <iterator>
#include <exception>
#include <sstream>

class AST_Decl;
class AST_Structure;

/**
 * Find Keys in Samples
 *
 * Use like this:
 * AST_Structure* struct_node;
 * // ...
 * SampleKeys keys(struct_node);
 * SampleKeys::Iterator end = keys.end();
 * for (SampleKeys::Iterator i = keys.begin(); i != end; ++i) {
 *   AST_Decl* key = *i;
 *   // ...
 * }
 *
 * The key AST_Decl will be a different type of node depending on the key:
 * - For struct field keys this will be the AST_Field
 * - For Array keys this will be the base AST_Type, repeated for each element
 * - For Union keys this will be the AST_Union
 */
class SampleKeys {
public:
  enum RootType {
    PrimitiveType,
    StructureType,
    ArrayType,
    UnionType,
    InvalidType
  };

  /**
   * Get the RootType of the AST_Type
   */
  static RootType root_type(AST_Type* type);

  /**
   * Error in the AST or the application of the @key annotation.
   */
  class Error : public std::exception {
  public:
    Error();
    Error(const Error& error);
    Error(const std::string& message);
    Error(AST_Decl* node, const std::string& message);

    Error& operator=(const Error& error);
    virtual const char* what() const noexcept;

  private:
    std::string message_;
  };

  /**
   * Iterator for traversing the TAO_IDL AST, looking for nodes within a sample
   * node that are annotated with @key.
   */
  class Iterator {
  public:
    /**
     * Standard Iterator Type Declarations
     */
    ///{
    typedef AST_Decl* value_type;
    typedef AST_Decl** pointer;
    typedef AST_Decl*& reference;
    typedef std::output_iterator_tag iterator_category;
    ///}

    /**
     * Create new iterator equal to SampleKey::end()
     */
    Iterator();

    /**
     * Create new iterator pointing to the first sample key or equal to
     * SampleKey::end() if there are no keys.
     */
    Iterator(SampleKeys &parent);

    /**
     * Create completely separate copy of another iterator
     */
    Iterator(const Iterator& other);

    ~Iterator();

    Iterator& operator=(const Iterator& other);
    Iterator& operator++(); // Prefix
    Iterator operator++(int); // Postfix
    value_type operator*() const;
    bool operator==(const Iterator& other) const;
    bool operator!=(const Iterator& other) const;

    /**
     * Get the path of the key in reference to the root_
     */
    std::string path();

    /**
     * Get the level of recursion
     */
    size_t level() const;

    /**
     * Get the root type of the final child
     */
    RootType root_type() const;

    /**
     * Get the final child's parent's root type
     *
     * Returns InvalidType if it is the root or a invalid iterator
     */
    RootType parents_root_type() const;

    /**
     * Get the AST_Type of the current value
     *
     * Returns 0 if the iterator is invalid
     */
    AST_Type* get_ast_type() const;

  private:
    Iterator(AST_Type* root, Iterator* parent);
    Iterator(AST_Field* root, Iterator* parent);

    /**
     * Position in whatever node we are in.
     *
     * This means different things for different types of nodes.
     */
    Iterator* parent_;
    size_t pos_;
    Iterator* child_;
    /// Current value of the entire iterator stack
    value_type current_value_;
    AST_Decl* root_;
    RootType root_type_;
    size_t level_;
    bool recursive_;

    /**
     * Internal Recursive Impl. of path()
     */
    void path_i(std::stringstream& ss);

    void cleanup();
  };

  /**
   * If recurive is false, do not recurse into other sturctures.
   */
  SampleKeys(AST_Structure* root, bool recursive = true);
  SampleKeys(AST_Union* root);
  ~SampleKeys();

  AST_Decl* root() const;
  RootType root_type() const;

  Iterator begin();
  Iterator end();

  /**
   * Count the keys in the sample
   */
  size_t count();

  bool recursive() const;

private:
  AST_Decl* root_;
  RootType root_type_;

  /// Cached Key Count
  ///{
  bool counted_;
  size_t count_;
  ///}

  /// Have iterators recurse into structures
  bool recursive_;
};
#endif
#endif
